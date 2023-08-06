# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from typing import List
from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE

from ibm_wos_utils.explainability.entity.constants import ExplanationType


class FeatureRange():
    def __init__(self, min: str = None, min_inclusive: bool = None, max: str = None, max_inclusive: bool = None):
        self.min = min
        self.min_inclusive = min_inclusive
        self.max = max
        self.max_inclusive = max_inclusive


class ExplanationFeature():
    def __init__(self, feature_name: str = None, weight: str = None, feature_range: FeatureRange = None, feature_value: str = None, importance: str = None, positions: List = None):
        self.feature_name = feature_name
        self.weight = weight
        self.feature_range = feature_range
        self.feature_value = feature_value
        self.importance = importance
        self.positions = positions


class Prediction():
    def __init__(self, value: str, explanation_features: List[ExplanationFeature] = [], probability=None):
        self.value = value
        self.probability = probability
        self.explanation_features = explanation_features


class LimeExplanation():
    def __init__(self, predictions=None, error=None):
        self.explanation_type = ExplanationType.LIME.value
        self.predictions = predictions
        self.error = error


class ErrorTarget:
    def __init__(self, error_type, error_name):
        self.type = error_type
        self.name = error_name


class Error():
    def __init__(self, code, message, vals=[], target=None):
        self.code = code
        self.message = message
        self.vals = vals
        self.target = target


class BaseResponseSchema(Schema):

    def value_exist(self, value):
        if type(value) in [bool, int, float]:
            return True
        if value:
            return True
        return False

    @post_dump
    def remove_empty_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if self.value_exist(value)}


class FeatureRangeSchema(BaseResponseSchema):
    min = fields.String()
    min_inclusive = fields.Boolean()
    max = fields.String()
    max_inclusive = fields.Boolean()

    @post_load
    def create_feature_range(self, data):
        return FeatureRange(**data)


class ExplanationFeatureSchema(BaseResponseSchema):
    feature_name = fields.String()
    weight = fields.Number()
    feature_range = fields.Nested(FeatureRangeSchema)
    feature_value = fields.String()
    importance = fields.String()
    positions = fields.List(fields.Raw())

    @post_load
    def create_explanation_feature(self, data):
        return ExplanationFeature(**data)

class PredictionSchema(BaseResponseSchema):
    value = fields.String()
    probability = fields.Number()
    explanation_features = fields.List(fields.Nested(ExplanationFeatureSchema))

    @post_load
    def create_prediction(self, data):
        return Prediction(**data)


class ErrorTargetSchema(BaseResponseSchema):
    type = fields.String()
    name = fields.String()


class ErrorSchema(BaseResponseSchema):
    code = fields.String()
    message = fields.String()
    vals = fields.List(fields.String())
    target = fields.Nested(ErrorTargetSchema)


class LimeExplanationSchema(BaseResponseSchema):
    explanation_type = fields.String()
    predictions = fields.List(fields.Nested(PredictionSchema))
    error = fields.Nested(ErrorSchema)

class PertinentPositive():
    def __init__(self, features: List[ExplanationFeature] = []):
        self.features = features


class PertinentNegative():
    def __init__(self, features: List[ExplanationFeature] = [], prediction=None, probability=None, is_pn_closest_point_to_pp=None):
        self.features = features
        self.prediction = prediction
        self.probability = probability
        self.is_pn_closest_point_to_pp = is_pn_closest_point_to_pp



class ContrastiveExplanation():
    def __init__(self, pertinent_positive, pertinent_negative=None, error=None):
        self.explanation_type = ExplanationType.CONTRASTIVE.value
        self.pertinent_positive = pertinent_positive
        self.pertinent_negative = pertinent_negative
        self.error = error

class PertinentPositiveSchema(BaseResponseSchema):
    features = fields.List(fields.Nested(ExplanationFeatureSchema))

    @post_load
    def create_pp(self, data):
        return PertinentPositive(**data)


class PertinentNegativeSchema(BaseResponseSchema):
    class Meta:
        unknown = EXCLUDE
    features = fields.List(fields.Nested(ExplanationFeatureSchema))
    prediction = fields.String()
    probability = fields.Number()
    is_pn_closest_point_to_pp = fields.Boolean()

    @post_load
    def create_pn(self, data):
        return PertinentNegative(**data)


class ContrastiveExplanationSchema(BaseResponseSchema):
    explanation_type = fields.String()
    pertinent_positive = fields.Nested(PertinentPositiveSchema)
    pertinent_negative = fields.Nested(PertinentNegativeSchema)
    error = fields.Nested(ErrorSchema)

class LimeCemExplanation():
    def __init__(self, predictions: List[Prediction] = None,  contrastive_explanation=None, error_lime: Error = None, error_cem: Error = None, controllable: str = None):
        self.predictions = predictions or []
        self.contrastive_explanation = contrastive_explanation
        self.error_lime = error_lime
        self.error_cem = error_cem
        self.controllable = controllable

    def add_prediction(self, prediction: Prediction):
        self.predictions.append(prediction)

class LimeCemExplanationSchema(BaseResponseSchema):
    predictions = fields.List(fields.Nested(PredictionSchema))
    error_lime = fields.Nested(ErrorSchema)
    error_cem = fields.Nested(ErrorSchema)
    contrastive_explanation = fields.Nested(ContrastiveExplanationSchema)
    controllable = fields.Boolean()

    @post_load
    def create_entity(self, data, **kwargs):
        data.pop("explanation_type", None)
        return LimeCemExplanation(**data)

