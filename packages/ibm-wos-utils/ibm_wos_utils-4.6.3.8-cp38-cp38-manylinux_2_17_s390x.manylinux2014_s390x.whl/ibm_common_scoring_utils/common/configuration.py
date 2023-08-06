# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
from ibm_common_scoring_utils.utils.constants import ModelType, ServiceProviderType, get_model_types, get_service_types

class Configuration():
    """
        Class responsible for setting and getting configuration information needed for scoring
        Eg:
        {
            "features":[],
            "prediction":"prediction",
            "probability":"probability,
            "model_type":"binary",
            "service_type": "wml",
            "credentials":{<credentials based on service type>},
            "scoring_url": "<scoring_url>",
        }
    """
    def __init__(self,configuration:dict):
        #Validate configuration
        self.validate_configuration(configuration)

        self.features = configuration.get("features")
        self.prediction = configuration.get("prediction") or "prediction"
        self.probability = configuration.get("probability") or "probability"
        self.schema = configuration.get("schema")
        self.model_type = configuration.get("model_type")
        self.credentials = configuration.get("credentials")
        self.service_type = configuration.get("service_type")
        self.scoring_url = configuration.get("scoring_url")

        #The following property is meant to be used for SPSS - in cases where the probability fields cannot be self detected
        self.class_probabilites = configuration.get("class_probabilities") or []
        self.class_labels = configuration.get("class_labels") or []

        #Meta fields can be used for scoring needs in case of WML and custom ML 
        self.meta_fields = configuration.get("meta_fields") or []

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self,value):
        if not isinstance(value,list) or len(value) == 0:
            raise ValueError("Features cannot be empty")
        self._features = value

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self,value):
        if ModelType(value) is  None:
            raise ValueError(f"Unsupported value type:{value} . Acceptable values are :{get_model_types()}")
        self._model_type = value

    @property
    def service_type(self):
        return self._service_type

    @service_type.setter
    def service_type(self,value):
        if ServiceProviderType(value) is  None:
            raise ValueError(f"Unsupported value type:{value} . Acceptable values are :{get_service_types()}")
        self._service_type = value


    @property
    def scoring_url(self):
        return self._scoring_url

    @scoring_url.setter
    def scoring_url(self,value):
        if value is None:
            raise ValueError("scoring_url cannot be empty")
        self._scoring_url = value


    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self,value):
        if not isinstance(value, dict):
            raise ValueError("credentials cannot be empty")
        self._credentials = value

            
    def validate_configuration(self,configuration):
        missing_values = []
       
        if configuration.get("features") is None:
            missing_values.append("features")

        if configuration.get("model_type") is None:
            missing_values.append("model_type")

        if configuration.get("service_type") is None :
             missing_values.append("service_type")

        if configuration.get("credentials") is None:
            if configuration.get("service_type") == ServiceProviderType.AZURE_SERVICE.value:
                configuration["credentials"] = {}
            else:
                missing_values.append("credentials")

        if configuration.get("scoring_url") is None:
            missing_values.append("scoring_url")

        service_type = configuration.get("service_type")
        model_type = configuration.get("model_type")

        # Check for probability only for WML and Custom ML for rest the probability column value will be probability as there is a coversion
        # involved for constructing probability column
        if service_type in [ServiceProviderType.WML.value,ServiceProviderType.CUSTOM_ML.value] and model_type != ModelType.REGRESSION.value:
            if configuration.get("probability") is None:
                missing_values.append("probability")

            if configuration.get("prediction") is None:
                missing_values.append("prediction")

        if len(missing_values) > 0:
            raise AttributeError("Missing configuration properties . Details :{}".format(missing_values))


class Credentials():
    """
        Class responsible for setting credentials
    """
    def __init__(self,credentials:dict):
        self.url = credentials.get("url")

        
        self.apikey = credentials.get("apikey")
        if self.apikey is None:
            self.apikey = credentials.get("api_key")

        #WML
        self.instance_id = credentials.get("instance_id")
        self.wml_location = credentials.get("wml_location")
        self.uid = credentials.get("uid") #Needed for wml_location:cpd_local
        self.zen_service_broker_secret = credentials.get("zen_service_broker_secret") #Needed for wml_location:cpd_local

        #Custom ML Provider
        self.auth_provider = credentials.get("auth_provider")
        self.auth_type = credentials.get("auth_type")
        self.username = credentials.get("username")
        self.password = credentials.get("password")
        self.auth_url = credentials.get("auth_url")

        #AWS 
        self.access_key_id = credentials.get("access_key_id")
        self.secret_access_key = credentials.get("secret_access_key")
        self.region = credentials.get("region")

        #Azure studio
        # Note : In case of Azure studio/service each deployment is associated with a api_key which is mapped to "token" in openscale world
        self.azure_token = credentials.get("token")

        #Azure service 
        #Note : In case of Azure service each deployment is associated with token /secondaryKey and having crendetials is not mandatory to have these credentials
        self.azure_secondary_key = credentials.get("secondaryKey")


       


        

        


