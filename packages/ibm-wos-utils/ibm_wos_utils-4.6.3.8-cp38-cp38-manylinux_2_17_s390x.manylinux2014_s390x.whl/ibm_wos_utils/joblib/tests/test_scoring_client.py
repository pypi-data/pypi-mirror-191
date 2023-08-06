# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2020, 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from ibm_wos_utils.joblib.clients.scoring_client import ScoringClient


spark = SparkSession.builder.appName("ScoringClient").getOrCreate()

class TestScoringClient(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    
    def validate_is_df_numeric_response(self,response, expected_response):
        for df_type in response:
            self.assertTrue(df_type in expected_response)


    def test_is_df_numeric_double_long(self):
        values = [[1,1.2],[2,2.2]]
        features = ["f1","f2"]
        input_df = spark.createDataFrame(values,schema=features)

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["bigint","double"])

        #Should return False
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertFalse(response)


    def test_is_df_numeric_double_int(self):
        values = [[1,1.2],[2,2.2]]
        features = ["f1","f2"]
        input_df = spark.createDataFrame(values,schema=features)
        input_df = input_df.withColumn("f1",input_df["f1"].cast("int"))

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["double","int"])

        #Should return False
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertFalse(response)


    def test_is_df_numeric_int_long(self):
        values = [[1,1],[2,2]]
        features = ["f1","f2"]
        input_df = spark.createDataFrame(values,schema=features)
        input_df = input_df.withColumn("f2",input_df["f2"].cast("int"))

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["bigint","int"])

        #Should return True
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertTrue(response)

    def test_is_df_numeric_double(self):
        values = [[1.0,1.1],[2.0,2.1]]
        features = ["f1","f2"]
        input_df = spark.createDataFrame(values,schema=features)

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["double","double"])

        #Should return True
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertTrue(response)


    def test_is_df_numeric_double_string(self):
        values = [[1.0,"1.1"],[2.0,"2.1"]]
        features = ["f1","f2"]
        input_df = spark.createDataFrame(values,schema=features)

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["double","string"])

        #Should return True
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertTrue(response)


    def test_is_df_numeric_double_string_int(self):
        values = [[1.0,"1.1",1],[2.0,"2.1",2]]
        features = ["f1","f2","f3"]
        input_df = spark.createDataFrame(values,schema=features)
        input_df = input_df.withColumn("f3",input_df["f3"].cast("integer"))

        #Check datatypes
        df_dtypes = list(set([col_dtype[1] for col_dtype in input_df.dtypes]))
        self.validate_is_df_numeric_response(df_dtypes,["double","string","int"])

        #Should return True
        response = ScoringClient.is_df_numeric(input_df,features=features)
        self.assertTrue(response)


    def test_check_for_dot_in_feature_names_with_dot(self):
        features = ["Sepal.Length","Sepal.Width","Petal.Length","Petal.Width"]
        expected_features = ["`Sepal.Length`","`Sepal.Width`","`Petal.Length`","`Petal.Width`"]
        new_features = ScoringClient.check_for_dot_in_feature_names(features)
        self.assertEquals(expected_features,new_features)


    def test_check_for_dot_in_feature_names_without_dot(self):
        features = ["Sepal_Length","Sepal_Width","Petal_Length","Petal_Width"]
        new_features = ScoringClient.check_for_dot_in_feature_names(features)
        self.assertEquals(features,new_features)






        
        



