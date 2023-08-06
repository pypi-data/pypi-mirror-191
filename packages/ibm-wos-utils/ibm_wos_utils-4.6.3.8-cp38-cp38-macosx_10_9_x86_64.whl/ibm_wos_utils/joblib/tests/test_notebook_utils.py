# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_wos_utils.joblib.tests.base_test_utils import BaseTestUtils
from ibm_wos_utils.joblib.utils import notebook_utils
from pyspark.sql import SparkSession


class TestNotebookUtils(BaseTestUtils):

    def test_generate_schema(self):
        spark = SparkSession.builder.appName("NotebookUtilsTest").getOrCreate()
        df = self.read_csv_resource_as_spark_df("gcr_feedback.csv", spark)
        label_col = "Risk"
        prediction_col = "predicted_label"
        probability_col = "probability"
        non_feature_cols = [label_col, prediction_col,
                            probability_col, "scoring_id", "scoring_timestamp"]
        feature_columns = [
            col for col in df.columns if col not in non_feature_cols]
        dtypes_dict = dict(df.dtypes)
        categorical_columns = [
            col for col in feature_columns if dtypes_dict[col] in ["string", "boolean"]]

        config_info = {
            "feature_columns": feature_columns,
            "categorical_columns": categorical_columns,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }
        notebook_utils.validate_config_info(config_info)

        # Generate common configuration
        common_configuration = notebook_utils.generate_schemas(df, config_info)

        # Validate the common configuration
        self.validate_common_configuration(common_configuration)

    def test_generate_schema_with_meta_fields(self):
        spark = SparkSession.builder.appName("NotebookUtilsTest").getOrCreate()
        df = self.read_csv_resource_as_spark_df("gcr_feedback.csv", spark)
        label_col = "Risk"
        prediction_col = "predicted_label"
        probability_col = "probability"
        protected_attributes = ["Age", "Sex"]
        non_feature_cols = [label_col, prediction_col, probability_col,
                            "scoring_id", "scoring_timestamp"] + protected_attributes
        feature_columns = [
            col for col in df.columns if col not in non_feature_cols]
        dtypes_dict = dict(df.dtypes)
        categorical_columns = [
            col for col in feature_columns if dtypes_dict[col] in ["string", "boolean"]]

        config_info = {
            "feature_columns": feature_columns,
            "categorical_columns": categorical_columns,
            "protected_attributes": protected_attributes,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }
        notebook_utils.validate_config_info(config_info)

        # Generate common configuration
        common_configuration = notebook_utils.generate_schemas(df, config_info)

        # Validate the common configuration
        self.validate_common_configuration(common_configuration)

        # Check that protected attributes are added with modeling role meta-field
        prot_attrs_in_schema = []
        for field in common_configuration["output_data_schema"]["fields"]:
            if field["name"] in protected_attributes:
                assert field["metadata"]["modeling_role"] == "meta-field"
                prot_attrs_in_schema.append(field["name"])
        assert all(attr in prot_attrs_in_schema for attr in protected_attributes), "Missing protected attributes {} from the output data schema.".format(
            list(set(protected_attributes)-set(prot_attrs_in_schema)))

    def test_validate_config_info_1(self):
        label_col = "Risk"
        prediction_col = "predicted_label"
        probability_col = "probability"
        protected_attributes = ["Age", "Sex"]
        feature_columns = ["Test.1", "Test.2"]

        config_info = {
            "feature_columns": feature_columns,
            "protected_attributes": protected_attributes,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }

        try:
            notebook_utils.validate_config_info(config_info)
            self.fail("Expected an exception")
        except Exception as ex:
            self.assertTrue("Test.1" in str(ex))
            self.assertTrue("Test.2" in str(ex))

    def test_validate_config_info_2(self):
        label_col = "Risk.1"
        prediction_col = "predicted_label.1"
        probability_col = "probability.1"
        feature_columns = ["Age", "Sex"]

        config_info = {
            "feature_columns": feature_columns,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }

        try:
            notebook_utils.validate_config_info(config_info)
            self.fail("Expected an exception")
        except Exception as ex:
            self.assertTrue(label_col in str(ex))
            self.assertTrue(prediction_col in str(ex))
            self.assertTrue(probability_col in str(ex))

    def test_validate_config_info_3(self):
        label_col = "Risk"
        prediction_col = "predicted_label"
        probability_col = "probability"
        protected_attributes = ["Test.1", "Test.2"]
        feature_columns = ["Age", "Sex"]

        config_info = {
            "feature_columns": feature_columns,
            "protected_attributes": protected_attributes,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }

        try:
            notebook_utils.validate_config_info(config_info)
            self.fail("Expected an exception")
        except Exception as ex:
            self.assertTrue("Test.1" in str(ex))
            self.assertTrue("Test.2" in str(ex))

    def test_validate_config_info_4(self):
        label_col = "Risk"
        prediction_col = "predicted_label"
        probability_col = "probability"
        class_probabilities = ["Probability.1", "Probability.2"]
        feature_columns = ["Age", "Sex"]

        config_info = {
            "feature_columns": feature_columns,
            "class_probabilities": class_probabilities,
            "label_column": label_col,
            "prediction": prediction_col,
            "problem_type": "binary",
            "probability": probability_col
        }

        try:
            notebook_utils.validate_config_info(config_info)
            self.fail("Expected an exception")
        except Exception as ex:
            self.assertTrue("Probability.1" in str(ex))
            self.assertTrue("Probability.2" in str(ex))

    def validate_common_configuration(self, common_configuration: dict):
        assert common_configuration is not None, "The common configuration is empty."
        assert "feature_columns" in common_configuration and len(
            common_configuration["feature_columns"]) > 0, "Missing feature_columns in the common configuration."
        assert "categorical_columns" in common_configuration and len(
            common_configuration["categorical_columns"]) > 0, "Missing categorical_columns in the common configuration."
        assert "label_column" in common_configuration, "Missing label_column in the common_configuration."
        assert "prediction" in common_configuration, "Missing prediction in the common_configuration."
        assert "problem_type" in common_configuration, "Missing problem_type in the common_configuration."
        assert "training_data_schema" in common_configuration, "Missing training_data_schema in the common_configuration."
        assert "input_data_schema" in common_configuration, "Missing input_data_schema in the common_configuration."
        assert "output_data_schema" in common_configuration, "Missing output_data_schema in the common_configuration."
