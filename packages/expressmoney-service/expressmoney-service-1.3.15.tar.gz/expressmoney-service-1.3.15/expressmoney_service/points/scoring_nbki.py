__all__ = ('ScoringNBKIPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class ScoringNBKICreateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    snils = serializers.CharField(max_length=64)
    phone_number = serializers.CharField()


class ScoringNBKIResponseContract(Contract):
    score = serializers.FloatField()


class ScoringMTSID(ID):
    _service = _SERVICE
    _app = 'scoring_nbki'
    _view_set = 'scoring'


class ScoringNBKIPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = ScoringMTSID()
    _create_contract = ScoringNBKICreateContract
    _response_contract = ScoringNBKIResponseContract
