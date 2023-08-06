__all__ = ('ScoringBeeLinePoint',)

from phonenumber_field.serializerfields import PhoneNumberField

from expressmoney_service.api import *

_SERVICE = 'services'


class ScoringBeeLineCreateContract(Contract):
    phone_number = PhoneNumberField()


class ScoringBeeLineResponseContract(Contract):
    score = serializers.FloatField()


class ScoringBeeLineID(ID):
    _service = _SERVICE
    _app = 'scoring_beeline'
    _view_set = 'score'


class ScoringBeeLinePoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = ScoringBeeLineID()
    _create_contract = ScoringBeeLineCreateContract
    _response_contract = ScoringBeeLineResponseContract
