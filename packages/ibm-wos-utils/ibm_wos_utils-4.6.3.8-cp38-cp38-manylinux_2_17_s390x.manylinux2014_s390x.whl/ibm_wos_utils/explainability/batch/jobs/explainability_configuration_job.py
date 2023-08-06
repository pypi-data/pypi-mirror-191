# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------
import time
import json
try:
    from pyspark.sql import SQLContext
except ImportError as e:
    pass
from ibm_wos_utils.joblib.clients.scoring_client import ScoringClient
from ibm_wos_utils.joblib.jobs.aios_spark_job import AIOSBaseJob
from ibm_wos_utils.joblib.utils.constants import *
from ibm_wos_utils.joblib.utils.db_utils import DbUtils
from ibm_wos_utils.joblib.utils.param_utils import get
from ibm_wos_utils.joblib.utils.table_utils import TableUtils
from ibm_wos_utils.explainability.utils.training_data_stats import \
    TrainingDataStats
from ibm_wos_utils.explainability.utils.perturbations import \
    Perturbations


class ExplainabilityConfigurationJob(AIOSBaseJob):
    """Spark job to create/validate tables and 
    generate Explainability stats and perturbations and score them
    if enable_online_learning flag is set"""

    def run_job(self):
        self.logger.info("Starting the Explainability Configuration job")
        self.logger.info(self.arguments)
        table_utils = TableUtils(self.spark, self.sc, self.arguments,
                                 self.storage_type, self.location_type, self.jdbc_connection_properties)
        tables_status, table_info_json = table_utils.create_table()
        self.save_data(self.arguments.get("output_file_path") +
                       "/tables_status.json", {"tables_status": tables_status})
        if table_info_json:
            self.save_data(self.arguments.get("output_file_path") +
                           "/table_info.json", table_info_json)

        enable_online_learning = get(self.arguments, "enable_online_learning")

        if enable_online_learning:
            self.logger.info(
                "Generating Explainability stats and perturbations")
            self.__generate_stats_and_perturbations()

    def __validate_and_set_params(self):
        # Validate training table
        tables = get(self.arguments, "tables", [])
        training_table = next((table for table in tables if get(
            table, "type", "") == "training"), None)
        if not training_table:
            raise Exception(
                "The database and/or table for reading training data is missing.")
        self.database = get(training_table, "database_name")
        self.table = get(training_table, "table_name")
        self.schema = get(training_table, "schema_name")
        self.type = get(training_table, "type") or None

        # Partition Information
        self.partition_column = get(
            training_table, "parameters.partition_column")
        self.num_partitions = get(
            training_table, "parameters.num_partitions", 1)

        if not self.database or not self.table:
            raise Exception(
                "The database and/or table for reading training data is missing.")

        self.feature_columns = get(self.arguments, "feature_columns", [])
        self.categorical_columns = get(
            self.arguments, "categorical_columns", [])

        if not self.feature_columns:
            raise Exception("No feature columns are added.")

        self.model_type = get(self.arguments, "problem_type")
        if self.model_type is None:
            self.model_type = get(self.arguments, "model_type")

        self.prediction_column = get(
            self.arguments, "prediction")
        self.probability_column = get(
            self.arguments, "probability")

        if not self.prediction_column:
            raise Exception(
                "The prediction column is missing from arguments.")
        if self.model_type != "regression" and not self.probability_column:
            raise Exception(
                "The probability column is missing from arguments.")

        self.label_column = get(
            self.arguments, "label_column")
        if not self.label_column:
            raise Exception("No label column is supplied.")

        self.record_timestamp_column = get(
            self.arguments, "record_timestamp")

        self.columns = self.feature_columns.copy()
        self.columns.append(self.prediction_column)
        self.columns.append(self.label_column)
        if self.probability_column is not None:
            self.columns.append(self.probability_column)
        if self.record_timestamp_column is not None:
            self.columns.append(self.record_timestamp_column)

        self.columns_to_filter = []
        if self.model_type != "regression":
            self.columns_to_filter.append(self.prediction_column)

    def __generate_explainability_config(self, spark_df):
        explainability_configuration = None
        perturbs_df = None
        self.logger.info("Explainability Configuration STARTED")
        explainability_configuration = TrainingDataStats(
            feature_columns=get(self.arguments, "feature_columns"),
            categorical_columns=get(self.arguments, "categorical_columns"),
            label_column=get(self.arguments, "label_column"),
            spark_df=spark_df).generate_explain_stats()
        training_stats_str = json.dumps(explainability_configuration)

        self.logger.info(
            "Storing the generated stats in training statistics json file")
        self.save_data(self.arguments.get("output_file_path") +
                       "/training_statistics.json", {"training_statistics": training_stats_str})
        output_data_schema={"fields": [{"name": k, "type": v.get("type")} for k, v in self.arguments.get("output_data_schema").items()]}
        perturbations = Perturbations(
            training_stats=explainability_configuration, problem_type=self.model_type, output_data_schema=output_data_schema)
        perturbs_df = perturbations.generate_perturbations()

        self.logger.info("Explainability Configuration COMPLETED")

        return explainability_configuration, perturbs_df

    def __generate_stats_and_perturbations(self):
        self.__validate_and_set_params()
        spark_df = DbUtils.get_table_as_dataframe(
            self.spark,
            self.location_type,
            self.database,
            self.table,
            schema_name=self.schema,
            columns_to_map=self.columns,
            columns_to_filter=self.columns_to_filter,
            connection_properties=self.jdbc_connection_properties,
            probability_column=self.probability_column,
            partition_column=self.partition_column,
            num_partitions=self.num_partitions)
        start_time = time.time()
        _, explain_perturbation_df = self.__generate_explainability_config(
            spark_df)
        response_df = None

        self.logger.info(
            "Scoring the generated perturbations using common scoring utility.")
        scoring_client = ScoringClient(service_type = get(self.arguments, "service_type"),
                                        model_type=get(self.arguments, "problem_type"),
                                        scoring_url=get(self.arguments, "scoring_url"),
                                        credentials=get(self.arguments, "credentials"),
                                        features=get(self.arguments, "feature_columns"),
                                        prediction=get(self.arguments, "prediction"),
                                        probability=get(self.arguments, "probability"),
                                        prediction_data_type=get(self.arguments, "prediction_data_type"),
                                        metafields=get(self.arguments, "meta_columns") or [],
                                        class_probabilities = get(self.arguments, "class_probabilities") or [],
                                        class_labels = get(self.arguments, "class_labels") or [])
        try:
            self.logger.info("field names {}".format(list(explain_perturbation_df.columns)))
            meta_fields = self.arguments.get("meta_columns")
            if meta_fields:
                meta_row = spark_df.select(meta_fields).first()
                meta_vals = [val for val in meta_row]
                explain_perturbation_df[meta_fields] = meta_vals
            spark_df = self.spark.createDataFrame(explain_perturbation_df, schema=list(explain_perturbation_df.columns))
            response_df = scoring_client.score(spark_df,include_features_in_response=False)
        except Exception as e:
            self.logger.warn(
                "scoring the perturbations failed with exception:{0} ", str(e))
        if not (response_df is None or len(response_df.head(1)) == 0):
            probabilities = []
            prediction = []

            for row in response_df.collect():
                if self.prediction_column in response_df.columns:
                    prediction.append(row[self.prediction_column])
                if self.probability_column in response_df.columns:
                    probabilities.append(row[self.probability_column])

            if get(self.arguments, "problem_type") == "regression":
                scoring_response = {"predictions": prediction}
            else:
                scoring_response = {
                    "predictions": prediction, "probabilities": probabilities}
            self.save_data(self.arguments.get("output_file_path") +
                           "/lime_scored_perturbations.json", scoring_response)
            self.logger.info("completed scoring the perturbations")
        self.logger.info("Completed Explainability configuration job.")

