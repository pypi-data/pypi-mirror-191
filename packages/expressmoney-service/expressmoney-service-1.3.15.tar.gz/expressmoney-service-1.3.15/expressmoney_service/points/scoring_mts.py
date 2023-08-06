__all__ = ('ScoringMTSPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class ScoringMTSCreateContract(Contract):
    phone_number = serializers.CharField()


class ScoringMTSResponseContract(Contract):
    score = serializers.FloatField()


class ScoringMTSID(ID):
    _service = _SERVICE
    _app = 'scoring_mts'
    _view_set = 'scoring'


class ScoringMTSPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = ScoringMTSID()
    _create_contract = ScoringMTSCreateContract
    _response_contract = ScoringMTSResponseContract
