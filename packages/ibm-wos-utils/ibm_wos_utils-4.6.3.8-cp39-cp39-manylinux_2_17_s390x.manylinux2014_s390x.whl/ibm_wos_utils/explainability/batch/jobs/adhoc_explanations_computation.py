# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021, 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------
import base64
import json
import tarfile
try:
    from pyspark import SparkFiles
except ImportError as e:
    pass

from ibm_wos_utils.joblib.jobs.aios_spark_job import AIOSBaseJob
from ibm_wos_utils.explainability.batch.utils.compute_explanation import ComputeExplanation
from ibm_wos_utils.joblib.utils.db_utils import DbUtils
from ibm_wos_utils.joblib.utils.joblib_utils import JoblibUtils
from ibm_wos_utils.joblib.utils.hive_utils import get_table_as_dataframe
from ibm_wos_utils.explainability.entity.explain_config import ExplainConfig
from ibm_wos_utils.explainability.batch.entity.subscription import Subscription
from ibm_wos_utils.explainability.batch.utils.explanations_store import ExplanationsStore
from ibm_common_scoring_utils.core.score_manager import ScoreManager
from ibm_wos_utils.joblib.utils.param_utils import get
from ibm_wos_utils.explainability.entity.constants import ExplanationType


class AdhocExplanationsComputation(AIOSBaseJob):

    def run_job(self):
        scoring_ids = []
        explanation_task_ids = []
        lime_explanations = {}
        try:
            # Initialize attributes
            config, score_response = self.get_job_data()
            explain_config = self.get_explain_config(
                config.get("explainability_configuration"))
            self.logger.info(
                "Explainability configuration is " + str(vars(explain_config)))
            subscription = Subscription(config.get("subscription"))
            self.logger.info("Subscription details are " + str(subscription))
            scoring_ids = self.arguments.get("scoring_ids")
            explanation_task_ids = self.arguments.get("explanation_task_ids")
            subscription.explain_result_ds.jdbc_connection_properties = self.jdbc_connection_properties


            payload_df = self.get_payload_df(
                explain_config=explain_config, subscription=subscription)

            rows, missing_rows = self.get_input_rows(
                scoring_ids, explanation_task_ids, payload_df, subscription)

            self.logger.info("Starting adhoc explanations computation task for subscription {} in datamart {}.".format(
                subscription.subscription_id, subscription.data_mart_id))

            explanation_types = explain_config.explanation_types
            store = ExplanationsStore(
                spark=self.spark, data_source=subscription.explain_result_ds, logger=self.logger)

            # If lime explanation doesn't already exist, generate new lime explanation
            if ExplanationType.LIME in explanation_types:
                self.logger.info("Checking if lime explanation already exists for the given scoring_id(s)")
                lime_explanations = self.__get_existing_lime_explanation(store, subscription)
                values = lime_explanations.get("values")
                if values is None or len(values) == 0:
                    # generate lime explanation
                    self.__generate_lime_explanation(explain_config, rows, store, score_response, subscription)
                    lime_explanations = self.__get_existing_lime_explanation(store, subscription)

            if  ExplanationType.CONTRASTIVE in explanation_types:
                # reuse the lime explanation in contrastive
                self.logger.info("starting contrastive explanation computation")
                decoded_lime_explanations = []
                try:
                    for i in range(len(lime_explanations.get("values"))):
                        lime_exp = lime_explanations.get("values")[i][8]
                        decoded_lime_explanations.append(json.loads(base64.b64decode(
                        lime_exp).decode("utf-8")))
                except Exception as e:
                    # If an error occurred while generating lime explanation, proceed with cem
                    pass
                explain_config.explanation_types = [ExplanationType.CONTRASTIVE.value]
                config = self.__get_config_for_score_utils(explain_config)
                score_manager = ScoreManager(configuration=config)
                compute_explanation = ComputeExplanation(
                    explain_config=explain_config, subscription=subscription, score_response=None, created_by=self.arguments.get("created_by"), score_manager=score_manager, lime_explanation=decoded_lime_explanations)
                if rows:
                    cem_explanations = self.sc.parallelize(rows).mapPartitions(
                        compute_explanation.compute)
                    store.store_explanations(cem_explanations)
                    self.logger.info("stored contrastive explanation in the explanation store")

            if missing_rows:
                explanations = self.sc.parallelize(
                    missing_rows).mapPartitions(compute_explanation.compute_no_record_explanation)
                store.store_explanations(explanations)

            self.logger.info("Completed adhoc explanations computation task for subscription {} in datamart {}.".format(
                subscription.subscription_id, subscription.data_mart_id))
            self.__save_explanations(
                store, subscription.subscription_id, explanation_task_ids, explanation_types, scoring_ids)
        except Exception as ex:
            self.logger.error(
                "An error occurred while running the explanations_computation job. " + str(ex))
            super().save_exception_trace(error_msg=str(ex))
            raise ex

    def finish_job(self):
        file_path = self.arguments.get(
            "data_file_path") + "/explain_job_data.tar.gz"
        JoblibUtils.delete_file_from_hdfs(self.spark, file_path)
        super().finish_job()

    def get_input_rows(self, scoring_ids, explanation_task_ids, payload_df, subscription):
        rows = []
        missing_rows = []
        for (scoring_id, task_id) in zip(scoring_ids, explanation_task_ids):
            row = payload_df.filter(
                payload_df[subscription.scoring_id_column] == scoring_id).take(1)
            if row:
                row = row[0].asDict()
                row["explanation_task_id"] = task_id
                rows.append(row)
            else:
                missing_rows.append({
                    subscription.scoring_id_column: scoring_id,
                    "explanation_task_id": task_id
                })
        self.logger.info("Input rows found: " + str(rows))
        self.logger.info("Missing input rows: " + str(missing_rows))
        return rows, missing_rows

    def __get_columns(self, explain_config, subscription):
        columns = explain_config.feature_columns.copy()
        if explain_config.prediction_column:
            columns.append(explain_config.prediction_column)
        if explain_config.probability_column:
            columns.append(explain_config.probability_column)
        if subscription.scoring_timestamp_column:
            columns.append(subscription.scoring_timestamp_column)
        columns.append(subscription.scoring_id_column)
        return columns

    def get_explain_config(self, config):

        return ExplainConfig(input_data_type=config.get("input_data_type"),
                             problem_type=config.get("problem_type"),
                             feature_columns=config.get("feature_columns"),
                             categorical_columns=config.get(
                                 "categorical_columns"),
                             prediction_column=config.get("prediction_column"),
                             probability_column=config.get(
                                 "probability_column"),
                             training_stats=config.get("training_statistics"),
                             schema=config.get("features_schema"),
                             features_count=config.get("features_count"),
                             perturbations_count=config.get(
                                 "perturbations_count"),
                             sample_around_instance=config.get(
                                 "sample_around_instance"),
                             discretize_continuous=config.get(
                                 "discretize_continuous"),
                             discretizer=config.get("discretizer"),
                             kernel_width=config.get("kernel_width"),
                             feature_selection=config.get("feature_selection"),
                             features_schema=config.get("features_schema"),
                             explanation_types=config.get("explanation_types"),
                             service_type=config.get("service_type"),
                             meta_fields=config.get("meta_columns"))

    def get_job_data(self):
        self.sc.addFile(self.arguments.get(
            "data_file_path") + "/explain_job_data.tar.gz")
        with tarfile.open(SparkFiles.get("explain_job_data.tar.gz")) as f:
            config = json.loads(f.extractfile("explain_config.json").read())
            perturbations_score_response = json.loads(
                f.extractfile("explain_scoring_response.json").read())
        return config, perturbations_score_response

    def get_payload_df(self, explain_config, subscription):
        scoring_ids = self.arguments.get("scoring_ids")

        # Read data from explanations queue table
        queue_table_rows = self.__get_payload(connection=subscription.explain_queue_ds.connection,
                                              database=subscription.explain_queue_ds.database,
                                              schema=subscription.explain_queue_ds.schema,
                                              table=subscription.explain_queue_ds.table,
                                              explain_config=explain_config,
                                              subscription=subscription,
                                              scoring_ids=scoring_ids)

        missing_scoring_ids = []
        for s in scoring_ids:
            if queue_table_rows.filter(queue_table_rows[subscription.scoring_id_column] == s).count() < 1:
                missing_scoring_ids.append(s)

        payload_table_rows = None
        if missing_scoring_ids and subscription.payload_ds.connection and subscription.payload_ds.table:
            self.logger.info(
                "Could not find scoring ids {} in explanation queue table. Searching in payload table.".format(missing_scoring_ids))

            # Read data from payload table
            payload_table_rows = self.__get_payload(connection=subscription.payload_ds.connection,
                                                    database=subscription.payload_ds.database,
                                                    schema=subscription.payload_ds.schema,
                                                    table=subscription.payload_ds.table,
                                                    explain_config=explain_config,
                                                    subscription=subscription,
                                                    scoring_ids=missing_scoring_ids)

        payload_df = queue_table_rows
        if payload_table_rows:
            payload_df = payload_df.union(payload_table_rows)

        return payload_df

    def __get_payload(self, connection, database, schema, table, explain_config, subscription, scoring_ids):
        connection_type = connection.get("type")
        if connection_type == "jdbc":
            # Read data from explanation queue table in db2
            search_query = "select * from \"{}\".\"{}\" where \"{}\" in ({})".format(
                schema, table, subscription.scoring_id_column, ",".join(["'{}'".format(i) for i in scoring_ids]))
            self.logger.info(
                "Getting payload data using query: {}".format(search_query))
            queue_table_rows = DbUtils.get_table_as_dataframe(spark=self.spark,
                                                              database_name=database,
                                                              schema_name=schema,
                                                              connection_properties=self.jdbc_connection_properties,
                                                              location_type=connection_type,
                                                              table_name=table, columns_to_map=self.__get_columns(
                                                                  explain_config, subscription),
                                                              sql_query=search_query,
                                                              probability_column=explain_config.probability_column)
        else:
            # Read data from explanation queue table in hive
            queue_table_rows = get_table_as_dataframe(spark=self.spark,
                                                      database_name=database,
                                                      table_name=table, columns_to_map=self.__get_columns(
                                                          explain_config, subscription),
                                                      columns_to_filter=[
                                                          subscription.scoring_id_column],
                                                      search_filters=["{}:in:{}".format(subscription.scoring_id_column, ",".join(scoring_ids))])

        return queue_table_rows

    def __save_explanations(self, store, subscription_id, explanation_task_ids, explanation_types, scoring_ids):

        is_task_id_generated = get(self.arguments, "is_task_id_generated")
        self.logger.info(
            "Getting explanations for the explanation task ids {} to store in datamart.".format(explanation_task_ids))

        search_filters = "subscription_id:eq:{},request_id:in:{}".format(subscription_id,
                                                                         ",".join(explanation_task_ids))
        response = store.get_explanations(
            search_filters=search_filters, order_by_column="finished_at:desc", limit=100)

        check_existing_lime = False
        if explanation_task_ids and not response.get("values"):
            check_existing_lime = True
        elif explanation_task_ids and response.get("values") and \
             (ExplanationType.CONTRASTIVE in explanation_types and len(response.get("values")) <=1):
            check_existing_lime = True

        if check_existing_lime:
            self.logger.info("getting existing lime explanation and updating request id to store in Openscale db")
            # If a lime explanation already exists for a given scoring id but has a different request id, 
            # store the explanation row in Openscale db with the given request id.

            search_filters = "subscription_id:eq:{},status:eq:{},explanation_type:eq:{},scoring_id:in:{}".format(subscription_id, "FINISHED", ExplanationType.LIME.value,
                                                                         ",".join(scoring_ids))
            resp = store.get_explanations(search_filters=search_filters, order_by_column="finished_at:desc", limit=1)
            # If multiple records with the same scoring id exist in the explanation table,
            # fetch the recent explanation for the given scoring id
            values = resp.get("values")
            if len(values) > 0:
                fields = resp.get("fields")
                request_id_index = fields.index("request_id")
                for val, explanation_task_id in zip(values, explanation_task_ids):
                    val[request_id_index] = explanation_task_id
                if not response.get("values"):
                    response["values"] = values.copy()
                    response["fields"] = fields
                else:
                    response.get("values").append(values[0].copy())
                self.logger.info("Completed updating request id for existing lime explanation")


        fields = response.get("fields")
        resp_values = response.get("values").copy()
        resp_values.sort(
            key=lambda x: x[fields.index("finished_at")], reverse=True)
        request_id_index = fields.index("request_id")
        explanation_type_index = fields.index("explanation_type")
        values = []
        for tid in explanation_task_ids:
            cem_exp_row =   next(
                    (v for v in resp_values if v[request_id_index] == tid and v[explanation_type_index] == ExplanationType.CONTRASTIVE.value), None)
            lime_exp_row = next(
                    (v for v in resp_values if v[request_id_index] == tid and v[explanation_type_index] == ExplanationType.LIME.value), None)
        
            if ExplanationType.CONTRASTIVE in explanation_types and is_task_id_generated:
                # save the lime explanation as well in the explanations json if 
                # explanation_types is only set to ["contrastive"] and task id is not sent 
                # in the post payload
                if cem_exp_row:
                    values.append(cem_exp_row)
                if lime_exp_row:
                    values.append(lime_exp_row)
            elif ExplanationType.CONTRASTIVE in explanation_types and not is_task_id_generated:
                # this is the case when UI calls the API twice(once for lime and then for contrastive) 
                # with same explanation task id
                # return only contrastive explanation in this case as lime is already returned in the first
                # call
                if cem_exp_row:
                    values.append(cem_exp_row)
            else:
                if lime_exp_row:
                    values.append(lime_exp_row)

        if values:
            response["values"] = values

        self.save_data(self.arguments.get(
            "output_file_path")+"/explanations.json", response)
        self.logger.info(
            "Completed getting explanations to store in datamart.")

    def __get_config_for_score_utils(self, explain_config):
        config = {
            "features": explain_config.feature_columns or [],
            "service_type": explain_config.service_type,
            "model_type": explain_config.problem_type.value,
            "scoring_url": get(self.arguments, "scoring_url"),
            "prediction": explain_config.prediction_column,
            "probability": explain_config.probability_column,
            "credentials": get(self.arguments, "credentials"),
            "meta_fields": explain_config.meta_fields,
            "class_probabilities": get(self.arguments, "class_probabilities"),
            "class_labels": get(self.arguments, "class_labels")
         }
        return config

    def __get_existing_lime_explanation(self, store, subscription):
        scoring_ids = self.arguments.get("scoring_ids")
        search_filters = "subscription_id:eq:{},status:eq:{},explanation_type:eq:{},{}:in:{}".format(subscription.subscription_id, "FINISHED", ExplanationType.LIME.value, subscription.scoring_id_column, ",".join(scoring_ids))
        lime_explanations = store.get_explanations(
            search_filters=search_filters, order_by_column="finished_at:desc", limit=len(scoring_ids))
        return lime_explanations

    def __generate_lime_explanation(self, explain_config, rows, store, score_response, subscription):
        self.logger.info("Starting lime explanation computation")
        explain_config.explanation_types = [ExplanationType.LIME.value]
        score_response_bc = self.sc.broadcast(score_response)
        compute_explanation = ComputeExplanation(
            explain_config=explain_config, subscription=subscription, score_response=score_response_bc, created_by=self.arguments.get("created_by"))
        if rows:
            lime_explanation = self.sc.parallelize(rows).mapPartitions(
                compute_explanation.compute)
            store.store_explanations(lime_explanation)
            self.logger.info("stored lime explanation in the explanation store")
        

