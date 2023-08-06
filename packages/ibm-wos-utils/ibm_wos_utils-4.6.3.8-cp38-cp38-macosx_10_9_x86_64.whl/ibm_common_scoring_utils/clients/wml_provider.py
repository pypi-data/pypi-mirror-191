# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from ibm_common_scoring_utils.clients.service_provider import ServiceProvider
from ibm_common_scoring_utils.common.configuration import Configuration
from ibm_common_scoring_utils.utils.auth_utils import get_cp4d_impersonated_token, get_cp4d_jwt_token, get_iam_token
from ibm_common_scoring_utils.utils.constants import AuthProvider, get_auth_providers
from ibm_common_scoring_utils.utils.python_utils import convert_df_to_list
from ibm_common_scoring_utils.utils.rest_util import RestUtil
from ibm_common_scoring_utils.utils.data_time_util import DateTimeUtil

import pandas as pd


class WMLProvider(ServiceProvider):
    def __init__(self,config:Configuration):
        super().__init__(config)

    
    def get_headers(self):
        """
            Get headers for WML
        """
        if self.credentials.wml_location in [AuthProvider.CLOUD.value, AuthProvider.CLOUD_REMOTE.value]:
            #Cloud
            token = get_iam_token(self.credentials.apikey)
        else:
            #CPD case
            if self.credentials.wml_location == AuthProvider.CPD_LOCAL.value:
                token = get_cp4d_impersonated_token(self.credentials.url,self.credentials.uid,self.credentials.zen_service_broker_secret)
            else:
                token = get_cp4d_jwt_token(self.credentials.url,username=self.credentials.username,apikey=self.credentials.apikey)

        headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

        return headers


    def __get_scoring_url(self):
        """
            Method to add version query parameter if it does not exist 
        """
        if self.config.scoring_url.find("?version=") != -1:
            return self.config.scoring_url
        else:
            #Add version param with a dummy value
            return self.config.scoring_url.strip() + "?version=2022-09-22"



    def score(self,df:pd.DataFrame):
        """
            Score WML deployment
        """
        try:
            scoring_payload = self.convert_df_to_request(df)

            start_time = DateTimeUtil.current_milli_time()

            scoring_url = self.__get_scoring_url()

            #Note 520,522 are the status codes for connection time out , we can extend the list if needed
            response = RestUtil.request(additional_retry_status_codes=[520,521,522,523,524]).post(
                    url=scoring_url,
                    headers=self.get_headers(),
                    json=scoring_payload,verify=False
            )

            self.logger.log_debug(f"Time taken to score wml deployment {DateTimeUtil.current_milli_time()-start_time}ms")

            if (not response.ok):
                raise Exception(f"Error while scoring WML deployment with url {scoring_url}.Error code:{response.status_code}.Reason:{response.text}")
            

            return self.convert_response_to_df(response.json())
        except Exception as ex:
            msg =f"Error while scoring WML .Reason:{str(ex)}"
            self.logger.log_error(msg)
            raise Exception(msg)


    def validate_credentials(self):
        """
            Validate WML credentials existence
            For cloud :
            {
                "wml_location": "cloud"/"cloud_remote",
                "apikey":"****",
                "auth_url": <optional (to work on non production env)>
            }

            For CPD with WML Remote:
            {
                "wml_location":"one of cpd_remote",
                "apikey":"****"
                "username":"admin",
                "url": "<host url>"
            }

            For CPD with WML Local:
            {
                "wml_location":"cpd_local",
                "uid":"****"
                "zen_service_borker_secret":"admin",
                "url": "<host url>"
            }
        """
        #Make wml_location as mandatory value
        if self.credentials.wml_location is None:
            raise KeyError(f"Missing WML location . Acceptable values are:{get_auth_providers()}")

        missing_values = []
        #api_key is need for coud , cloud_remote , cpd_remote
        if self.credentials.apikey is None  and not (self.credentials.wml_location == AuthProvider.CPD_LOCAL.value):
             missing_values.append("apikey")

        if self.credentials.wml_location == AuthProvider.CPD_REMOTE.value:
            if self.credentials.username is None:
                missing_values.append("username")

            if self.credentials.url is None:
                missing_values.append("url")

        #Check for wml_location : cpd_local
        if self.credentials.wml_location == AuthProvider.CPD_LOCAL.value:
            #uid and zen_service_broker_secret has to coexist
            if self.credentials.uid == None:
                missing_values.append("uid")
            
            if self.credentials.zen_service_broker_secret == None:
                missing_values.append("zen_service_broker_secret")

        if len(missing_values) > 0:
            raise KeyError(f"Missing credentials information.Keys information:{missing_values}")


    def convert_df_to_request(self,df:pd.DataFrame) -> dict:
        """
            Convert spark dataframe to WML request
        """
        start_time = DateTimeUtil.current_milli_time()
        fields = self.config.features
        values = convert_df_to_list(df,fields)

        scoring_payload = {"input_data":[{
            "fields":fields,
            "values":values
            }]}

        #Construct meta info
        if len(self.config.meta_fields) > 0:
            meta_fields = self.config.meta_fields
            meta_values = convert_df_to_list(df,meta_fields)
            meta_payload = {
                "fields":meta_fields,
                "values":meta_values
            }
            scoring_payload["input_data"][0]["meta"] = meta_payload
            
        self.logger.log_debug(f"Completed constructing scoring request in {DateTimeUtil.current_milli_time()-start_time}ms")
        return scoring_payload


    def convert_response_to_df(self,response:dict) -> pd.DataFrame:
        """
             Convert response to spark dataframe
        """
        start_time = DateTimeUtil.current_milli_time()
        predictions = response.get("predictions")[0]

        #Extract only prediction and probability
        fields = predictions.get("fields")
        values = predictions.get("values")

        if len(fields) in [1,2]:  # Considering regression and classification cases respectively
            #No need of additional extraction
            response_df = pd.DataFrame(values,columns=fields)
        else:
            #Extract only prediction and probability to avoid conversion problems
            try:
                prediction_column_index = fields.index(self.config.prediction)
                probability_column_index = fields.index(self.config.probability)
            except Exception as ex:
                msg = f"Error detecting prediction/probability column index. Response field are:{fields}"
                self.logger.log_warning(msg)
                raise Exception(msg)
        
            response1 =[[value[prediction_column_index],value[probability_column_index]]for value in values]
            response_df = pd.DataFrame(response1,columns=[self.config.prediction,self.config.probability])


        self.logger.log_debug(f"Completed converting  scoring response to datafame in {DateTimeUtil.current_milli_time()-start_time}ms")
        return response_df