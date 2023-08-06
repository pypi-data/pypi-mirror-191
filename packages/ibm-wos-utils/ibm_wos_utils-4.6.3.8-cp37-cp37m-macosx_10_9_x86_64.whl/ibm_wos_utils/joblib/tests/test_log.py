import json
import logging
import logging.config
import pathlib
import unittest
import copy

from ibm_wos_utils.joblib.utils.log_formatter import SensitiveDataFormatter, SENSITIVE_FIELDS


class TestLog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def get_logger(self):
        clients_dir = pathlib.Path(__file__).parent.absolute()
        with open(str(clients_dir) + "/../jobs/logging.json", "r") as f:
            log_config = json.load(f)
        logging.config.dictConfig(log_config)
        for h in logging.root.handlers:
            h.setFormatter(SensitiveDataFormatter(
                h.formatter))

        return logging.getLogger(__name__)

    def test_logger(self):
        logger = self.get_logger()
        # Test logging hive related sensitive info
        params = {"storage": {"type": "hive",
                              "connection": {"metastore_url": "thrift://sample.host.com:9083", "location_type": "metastore"}}}
        original_params = copy.deepcopy(params)
        logger.info('AIOS base job parameters: {}'.format(params))
        # Verifying that original params dict is not modified after logging
        for field in params:
            assert params[field] == original_params[field]

        # Test logging jdbc related sensitive info
        params = {"storage": {"type": "jdbc",
                              "connection": {"jdbc_url": "jdbc:db2//host:50001/DB", "use_ssl": True, "certificate": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURFakNDQWZxZ0F3SUJBZ0lKQVA1S0R3ZTNCTkxiTUEwR0NTcUdTSWIzRFFFQkN3VUFNQjR4SERBYUJnTlYKQkFNTUUwbENUU0JEYkc5MVpDQkVZWFJoWW1GelpYTXdIaGNOTWpBd01qSTVNRFF5TVRBeVdoY05NekF3TWpJMgpNRFF5TVRBeVdqQWVNUnd3R2dZRFZRUUREQk5KUWswZ1EyeHZkV1FnUkdGMFlXSmhjMlZ6TUlJQklqQU5CZ2txCmhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdXUvbitpWW9xdkdGNU8xSGpEalpsK25iYjE4UkR4ZGwKTzRUL3FoUGMxMTREY1FUK0plRXdhdG13aGljTGxaQnF2QWFMb1hrbmhqSVFOMG01L0x5YzdBY291VXNmSGR0QwpDVGcrSUsxbjBrdDMrTHM3d1dTakxqVE96N3M3MlZUSU5yYmx3cnRIRUlvM1JWTkV6SkNHYW5LSXdZMWZVSUtrCldNMlR0SDl5cnFsSGN0Z2pIUlFmRkVTRmlYaHJiODhSQmd0amIva0xtVGpCaTFBeEVadWNobWZ2QVRmNENOY3EKY21QcHNqdDBPTnI0YnhJMVRyUWxEemNiN1hMSFBrWW91SUprdnVzMUZvaTEySmRNM1MrK3labFZPMUZmZkU3bwpKMjhUdGJoZ3JGOGtIU0NMSkJvTTFSZ3FPZG9OVm5QOC9EOWZhamNNN0lWd2V4a0lSOTNKR1FJREFRQUJvMU13ClVUQWRCZ05WSFE0RUZnUVVlQ3JZanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3SHdZRFZSMGpCQmd3Rm9BVWVDclkKanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRgpBQU9DQVFFQUkyRTBUOUt3MlN3RjJ2MXBqaHV4M0lkWWV2SGFVSkRMb0tPd0hSRnFSOHgxZ2dRcGVEcFBnMk5SCkx3R08yek85SWZUMmhLaWd1d2orWnJ5SGxxcHlxQ0pLOHJEU28xZUVPekIyWmE2S1YrQTVscEttMWdjV3VHYzMKK1UrVTFzTDdlUjd3ZFFuVjU0TVU4aERvNi9sVHRMRVB2Mnc3VlNPSlFDK013ejgrTFJMdjVHSW5BNlJySWNhKwozM0wxNnB4ZEttd1pLYThWcnBnMXJ3QzRnY3dlYUhYMUNEWE42K0JIbzhvWG5YWkh6UG91cldYS1BoaGdXZ2J5CkNDcUdIK0NWNnQ1eFg3b05NS3VNSUNqRVZndnNLWnRqeTQ5VW5iNVZZbHQ0b1J3dTFlbGdzRDNjekltbjlLREQKNHB1REFvYTZyMktZZE4xVkxuN3F3VG1TbDlTU05RPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
                                             "location_type": "jdbc"}, "credentials": {"username": "username", "password": "password"}}}
        original_params = copy.deepcopy(params)
        logger.warning(params)
        for field in params:
            assert params[field] == original_params[field]

    def test_mask_sensitive_fields(self):
        fields_to_mask = ["metastore_url", "username",
                          "password", "certificate", "apikey"]
        log_formatter = SensitiveDataFormatter(None)

        params = {"storage": {"type": "hive",
                              "connection": {"metastore_url": "thrift://sample.host.com:9083", "location_type": "metastore"}}}
        message = "AIOS base job parameters: {}".format(params)
        formatted_message = log_formatter.mask_sensitive_fields(
            message, fields_to_mask)
        for field in fields_to_mask:
            if field in message:
                assert "'{}': '***'".format(field) in formatted_message
        assert formatted_message == "AIOS base job parameters: {'storage': {'type': 'hive', 'connection': {'metastore_url': '***', 'location_type': 'metastore'}}}"

        params = {"storage": {"type": "jdbc",
                              "connection": {"jdbc_url": "jdbc:db2//host:50001/DB", "use_ssl": True, "certificate": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURFakNDQWZxZ0F3SUJBZ0lKQVA1S0R3ZTNCTkxiTUEwR0NTcUdTSWIzRFFFQkN3VUFNQjR4SERBYUJnTlYKQkFNTUUwbENUU0JEYkc5MVpDQkVZWFJoWW1GelpYTXdIaGNOTWpBd01qSTVNRFF5TVRBeVdoY05NekF3TWpJMgpNRFF5TVRBeVdqQWVNUnd3R2dZRFZRUUREQk5KUWswZ1EyeHZkV1FnUkdGMFlXSmhjMlZ6TUlJQklqQU5CZ2txCmhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdXUvbitpWW9xdkdGNU8xSGpEalpsK25iYjE4UkR4ZGwKTzRUL3FoUGMxMTREY1FUK0plRXdhdG13aGljTGxaQnF2QWFMb1hrbmhqSVFOMG01L0x5YzdBY291VXNmSGR0QwpDVGcrSUsxbjBrdDMrTHM3d1dTakxqVE96N3M3MlZUSU5yYmx3cnRIRUlvM1JWTkV6SkNHYW5LSXdZMWZVSUtrCldNMlR0SDl5cnFsSGN0Z2pIUlFmRkVTRmlYaHJiODhSQmd0amIva0xtVGpCaTFBeEVadWNobWZ2QVRmNENOY3EKY21QcHNqdDBPTnI0YnhJMVRyUWxEemNiN1hMSFBrWW91SUprdnVzMUZvaTEySmRNM1MrK3labFZPMUZmZkU3bwpKMjhUdGJoZ3JGOGtIU0NMSkJvTTFSZ3FPZG9OVm5QOC9EOWZhamNNN0lWd2V4a0lSOTNKR1FJREFRQUJvMU13ClVUQWRCZ05WSFE0RUZnUVVlQ3JZanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3SHdZRFZSMGpCQmd3Rm9BVWVDclkKanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRgpBQU9DQVFFQUkyRTBUOUt3MlN3RjJ2MXBqaHV4M0lkWWV2SGFVSkRMb0tPd0hSRnFSOHgxZ2dRcGVEcFBnMk5SCkx3R08yek85SWZUMmhLaWd1d2orWnJ5SGxxcHlxQ0pLOHJEU28xZUVPekIyWmE2S1YrQTVscEttMWdjV3VHYzMKK1UrVTFzTDdlUjd3ZFFuVjU0TVU4aERvNi9sVHRMRVB2Mnc3VlNPSlFDK013ejgrTFJMdjVHSW5BNlJySWNhKwozM0wxNnB4ZEttd1pLYThWcnBnMXJ3QzRnY3dlYUhYMUNEWE42K0JIbzhvWG5YWkh6UG91cldYS1BoaGdXZ2J5CkNDcUdIK0NWNnQ1eFg3b05NS3VNSUNqRVZndnNLWnRqeTQ5VW5iNVZZbHQ0b1J3dTFlbGdzRDNjekltbjlLREQKNHB1REFvYTZyMktZZE4xVkxuN3F3VG1TbDlTU05RPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
                                             "location_type": "jdbc"}, "credentials": {"username": "user", "password": "passw0rd"}}}
        message = "AIOS base job parameters: {}".format(params)
        formatted_message = log_formatter.mask_sensitive_fields(
            message, fields_to_mask)

        for field in fields_to_mask:
            if field in message:
                assert "'{}': '***'".format(field) in formatted_message

        assert formatted_message == "AIOS base job parameters: {'storage': {'type': 'jdbc', 'connection': {'jdbc_url': 'jdbc:db2//host:50001/DB', 'use_ssl': True, 'certificate': '***', 'location_type': 'jdbc'}, 'credentials': {'username': '***', 'password': '***'}}}"

        # Logging with json.dumps()
        formatted_message = log_formatter.mask_sensitive_fields(
            json.dumps(params), fields_to_mask)
        assert formatted_message == '{"storage": {"type": "jdbc", "connection": {"jdbc_url": "jdbc:db2//host:50001/DB", "use_ssl": true, "certificate": "***", "location_type": "jdbc"}, "credentials": {"username": "***", "password": "***"}}}'

        # Test with empty/none value in sensitive fields
        params = {"storage": {"type": "jdbc",
                              "connection": {"jdbc_url": "jdbc:db2//host:50001/DB", "use_ssl": True, "certificate": "",
                                             "location_type": "jdbc"}, "credentials": {"username": "username", "password": None}}}
        message = "AIOS base job parameters: {}".format(params)
        formatted_message = log_formatter.mask_sensitive_fields(
            message, fields_to_mask)
        assert formatted_message == "AIOS base job parameters: {'storage': {'type': 'jdbc', 'connection': {'jdbc_url': 'jdbc:db2//host:50001/DB', 'use_ssl': True, 'certificate': '***', 'location_type': 'jdbc'}, 'credentials': {'username': '***', 'password': None}}}"

        # check plain message
        message = "Sample log message"
        formatted_message = log_formatter.mask_sensitive_fields(
            message, fields_to_mask)
        assert formatted_message == message

        # Check message containing service provider credentials
        params = {'subscription': {'entity': {'analytics_engine': {'integrated_system_id': 'e30bafdb-03c0-4334-8190-7ee818a9c300', 'parameters': {'driver_cores': 1, 'driver_memory': 1, 'executor_cores': 1, 'executor_memory': 1, 'max_num_executors': 1, 'min_num_executors': 1}, 'type': 'spark'}, 'asset': {'asset_id': 'b330874076d0c41969a82aff7de5835f', 'asset_type': 'model', 'created_at': '2019-11-08T14:36:09.116Z', 'input_data_type': 'structured', 'name': 'neelima-admit-predict-linear-regression-2019-11-08-14-31-02', 'problem_type': 'regression', 'url': 's3://arsuryan-s3-bucket/sagemaker/admission-predict/neelima-admit-predict-linear-regression-2019-11-08-14-31-02/output/model.tar.gz'}, 'asset_properties': {'categorical_fields': [], 'dashboard_configuration': {'monitor_preparation': {'completed': True, 'file_name': 'configuration_archive.tar.gz'}}, 'feature_fields': ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'CGPA', 'Research'], 'input_data_schema': {'fields': [{'metadata': {'modeling_role': 'feature'}, 'name': 'GRE Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'TOEFL Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'University Rating', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'SOP', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'LOR', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'CGPA', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'Research', 'nullable': True, 'type': 'long'}], 'type': 'struct'}, 'label_column': 'Chance of Admit', 'output_data_schema': {'fields': [{'metadata': {'modeling_role': 'feature'}, 'name': 'GRE Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'TOEFL Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'University Rating', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'SOP', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'LOR', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'CGPA', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'Research', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'prediction'}, 'name': 'score', 'nullable': True, 'type': 'double'}, {'metadata': {'columnInfo': {'columnLength': 128}, 'modeling_role': 'record-id', 'primary_key': True}, 'name': 'scoring_id', 'nullable': False, 'type': 'string'}, {'metadata': {'modeling_role': 'record-timestamp'}, 'name': 'scoring_timestamp', 'nullable': False, 'type': 'timestamp'}, {'metadata': {}, 'name': 'deployment_id', 'nullable': False, 'type': 'string'}, {'metadata': {}, 'name': 'asset_revision', 'nullable': True, 'type': 'string'}], 'type': 'struct'}, 'predicted_target_field': '**N/A**', 'training_data_schema': {'fields': [{'metadata': {'modeling_role': 'feature'}, 'name': 'GRE Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'TOEFL Score', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'University Rating', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'SOP', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'LOR', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'CGPA', 'nullable': True, 'type': 'double'}, {'metadata': {'modeling_role': 'feature'}, 'name': 'Research', 'nullable': True, 'type': 'long'}, {'metadata': {'modeling_role': 'target'}, 'name': 'Chance of Admit', 'nullable': True, 'type': 'double'}], 'type': 'struct'}}, 'data_mart_id': '00000000-0000-0000-0000-000000000000', 'data_sources': [{'auto_create': False, 'connection': {'integrated_system_id': 'b193b7da-5d4b-4c8d-9204-15c86cea446f', 'type': 'jdbc'}, 'database_name': 'BLUDB', 'parameters': {}, 'schema_name': 'BATCH_EXPLAIN', 'status': {'state': 'active'}, 'table_name': 'payload_table_admit_predict_regression', 'type': 'payload'}, {'auto_create': False, 'connection': {'integrated_system_id': 'b193b7da-5d4b-4c8d-9204-15c86cea446f', 'type': 'jdbc'}, 'database_name': 'BLUDB', 'parameters': {}, 'schema_name': 'BATCH_EXPLAIN', 'status': {'state': 'active'}, 'table_name': 'feedback_table_admit_predict_regression', 'type': 'feedback'}], 'deployment': {'created_at': '2019-11-08T14:37:22.643Z', 'deployment_id': '155b20136d20663b08010f148e279a8c', 'deployment_type': 'batch', 'description': 'Created by feedback automation E2E_AWS_AdmitPredictRegression', 'name': 'admit-predict-regression-endpoint-201911081437', 'scoring_endpoint': {'request_headers': {'Content-Type': 'application/json'}, 'url': 'admit-predict-regression-endpoint-201911081437'}, 'url': 'admit-predict-regression-endpoint-201911081437'}, 'service_provider_id': '04e899e6-4b9d-4f56-9ead-87444eb179f8', 'status': {'state': 'active'}}, 'metadata': {'created_at': '2022-09-22T11:25:32.550Z', 'created_by': 'admin', 'crn': 'crn:v1:bluemix:public:aiopenscale:us-south:a/na:00000000-0000-0000-0000-000000000000:subscription:0e88d05d-df27-4900-bdb5-678495e38828', 'id': '0e88d05d-df27-4900-bdb5-678495e38828', 'modified_at': '2022-09-22T11:27:58.626Z', 'modified_by': 'admin', 'url': '/v2/subscriptions/0e88d05d-df27-4900-bdb5-678495e38828'}}, 'monitor_instance': {'entity': {'data_mart_id': '00000000-0000-0000-0000-000000000000', 'monitor_definition_id': 'fairness', 'parameters': {'favourable_class': [[0, 0.5]], 'features': [{'feature': 'GRE Score', 'majority': [[300, 400]], 'metric_ids': ['fairness_value', 'statistical_parity_difference'], 'minority': [[100, 299]], 'threshold': 0.8}], 'perform_perturbation': True, 'sample_size_percent': 75, 'unfavourable_class': [[0.6, 1]]}, 'schedule': {'repeat_interval': 1, 'repeat_type': 'week', 'repeat_unit': 'week', 'start_time': {'delay': 10, 'delay_unit': 'minute', 'type': 'relative'}, 'status': 'enabled'}, 'schedule_id': '2fbcc6fe-226f-4e52-8f66-71e08a4da360', 'status': {'state': 'active'}, 'target': {'target_id': '0e88d05d-df27-4900-bdb5-678495e38828', 'target_type': 'subscription'}, 'thresholds': [{'metric_id': 'fairness_value', 'specific_values': [{'applies_to': [{'key': 'feature', 'type': 'tag', 'value': 'GRE Score'}], 'value': 80.0}], 'type': 'lower_limit', 'value': 80.0}, {'metric_id': 'statistical_parity_difference', 'specific_values': [{'applies_to': [{'key': 'feature', 'type': 'tag', 'value': 'GRE Score'}], 'value': -0.15}], 'type': 'lower_limit', 'value': -0.15}, {'metric_id': 'statistical_parity_difference', 'specific_values': [{'applies_to': [{'key': 'feature', 'type': 'tag', 'value': 'GRE Score'}], 'value': 0.15}], 'type': 'upper_limit', 'value': 0.15}]}, 'metadata': {'created_at': '2022-09-22T11:27:21.828Z', 'created_by': 'admin', 'crn': 'crn:v1:bluemix:public:aiopenscale:us-south:a/na:00000000-0000-0000-0000-000000000000:monitor_instance:4bc31881-5286-4874-afca-2fb15f0b3d68', 'id': '4bc31881-5286-4874-afca-2fb15f0b3d68', 'modified_at': '2022-09-22T11:31:01.965Z', 'modified_by': 'internal-service', 'url': '/v2/monitor_instances/4bc31881-5286-4874-afca-2fb15f0b3d68'}}, 'subscription_id': '0e88d05d-df27-4900-bdb5-678495e38828', 'monitoring_run_id': '90a0665d-329c-4114-b81c-6f00e96756f2', 'storage': {'type': 'jdbc', 'connection': {'jdbc_url': 'jdbc:db2://48a34098-6865-436f-81ee-5f8ae202094a.bpe60pbd01oinge4psd0.databases.appdomain.cloud:32170/bludb', 'jdbc_driver': 'com.ibm.db2.jcc.DB2Driver', 'use_ssl': True, 'certificate': '', 'location_type': 'jdbc'}, 'credentials': {'username': '***', 'password': '***'}}, 'service_provider': {'entity': {'credentials': {'secret_id': '76bd8196-b84b-4517-80b0-b36d8ab51c54'}, 'name': 'AWS_EAST2_PROD', 'service_type': 'amazon_sagemaker', 'status': {'state': 'active'}}, 'metadata': {'created_at': '2022-09-15T07:10:43.571Z', 'created_by': 'admin', 'crn': 'crn:v1:bluemix:public:aiopenscale:us-south:a/na:00000000-0000-0000-0000-000000000000:service_provider:04e899e6-4b9d-4f56-9ead-87444eb179f8', 'id': '04e899e6-4b9d-4f56-9ead-87444eb179f8', 'url': '/v2/service_providers/04e899e6-4b9d-4f56-9ead-87444eb179f8'}}, 'service_provider_credentials': {'access_key_id': 'test_access_key', 'region': 'us-east-2', 'secret_access_key': 'test_secret_key'}, 'spark_settings': {'driver_cores': 1, 'driver_memory': 1, 'executor_cores': 1, 'executor_memory': 1, 'max_num_executors': 1, 'min_num_executors': 1}, 'output_file_path': 'hdfs://cornell1.fyre.ibm.com:9000/sw/openscale/group_bias_computation_0e88d05d-df27-4900-bdb5-678495e38828/0e88d05d-df27-4900-bdb5-678495e38828/output/90a0665d-329c-4114-b81c-6f00e96756f2', 'data_file_path': 'hdfs://cornell1.fyre.ibm.com:9000/sw/openscale/group_bias_computation_0e88d05d-df27-4900-bdb5-678495e38828/0e88d05d-df27-4900-bdb5-678495e38828/data', 'param_file_name': 'tmpej3b62fn'}
        message = "AIOS base job parameters: {}".format(params)
        formatted_message = log_formatter.mask_sensitive_fields(
            message, SENSITIVE_FIELDS)

        for field in SENSITIVE_FIELDS:
            if field in message and field in formatted_message:
                assert "'{}': '***'".format(field) in formatted_message

        logger = self.get_logger()
        logger.warning(message)


if __name__ == '__main__':
    unittest.main()
