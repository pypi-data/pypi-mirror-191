__all__ = ('ContractCreateStatusPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class ContractStatusCreateContract(Contract):
    inn = serializers.CharField(max_length=32)


class ContractStatusResponseContract(Contract):
    status = serializers.CharField(max_length=16)


class _ContractUpdateID(ID):
    _service = _SERVICE
    _app = 'contracts'
    _view_set = 'contract_status'


class ContractCreateStatusPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _ContractUpdateID()
    _create_contract = ContractStatusCreateContract
    _response_contract = ContractStatusResponseContract
