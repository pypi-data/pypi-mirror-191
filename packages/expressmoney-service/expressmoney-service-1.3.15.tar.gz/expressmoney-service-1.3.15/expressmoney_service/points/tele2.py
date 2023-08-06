__all__ = ('Tele2Point',)

from phonenumber_field.serializerfields import PhoneNumberField

from expressmoney_service.api import *

_SERVICE = 'services'
_APP = 'tele2'

EMPTY = 'EMPTY'
SUCCESS = 'SCS'
FAILURE = 'FAIL'

RESULT_CHOICES = (
    (EMPTY, EMPTY),
    (FAILURE, FAILURE),
    (SUCCESS, SUCCESS),
)


class _Tele2CreateContract(Contract):
    username = serializers.CharField()
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32, allow_blank=True)
    doc_series = serializers.CharField(max_length=4)
    doc_number = serializers.CharField(max_length=6)
    birth_date = serializers.DateField()


class _Tele2ResponseContract(Contract):
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    comment = serializers.CharField(max_length=256)


class _Tele2ID(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'verification'


class Tele2Point(CreatePointMixin, ResponseMixin,ContractPoint):
    _point_id = _Tele2ID()
    _create_contract = _Tele2CreateContract
    _response_contract = _Tele2ResponseContract
