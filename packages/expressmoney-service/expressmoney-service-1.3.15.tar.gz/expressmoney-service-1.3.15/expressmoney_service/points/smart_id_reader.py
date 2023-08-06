__all__ = ('PassportReaderPoint',)

from ..api import *

_SERVICE = 'services'
_APP = 'smart_id_reader'

EMPTY = 'EMPTY'
SUCCESS = 'SCS'
FAILURE = 'FAIL'

RESULT_CHOICES = (
    (EMPTY, EMPTY),
    (FAILURE, FAILURE),
    (SUCCESS, SUCCESS),
)


class PassportReaderCreateContract(Contract):
    file = serializers.FileField()


class PassportReaderResponseContract(Contract):
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    data = serializers.JSONField(allow_null=True)


class _PassportReader(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'passport_reader'


class PassportReaderPoint(UploadFilePointMixin, ResponseMixin, ContractPoint):
    _point_id = _PassportReader()
    _create_contract = PassportReaderCreateContract
    _response_contract = PassportReaderResponseContract
