__all__ = ('RuVerificatorPoint',)

from expressmoney_service.api import *
from phonenumber_field.serializerfields import PhoneNumberField

_SERVICE = 'services'


class RuVerificatorId(ID):
    _service = _SERVICE
    _app = "ru_verificator"
    _view_set = "verification_init"


class RuVerificatorCreateContract(Contract):
    user_id = serializers.IntegerField()
    phonenumber = PhoneNumberField(allow_null=True)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField(allow_null=True)
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16, help_text='Government department code')
    passport_date = serializers.DateField(allow_null=True)


class RuVerificatorResponseContract(Contract):
    is_verified = serializers.BooleanField()
    comment = serializers.CharField(max_length=512, allow_blank=True)


class RuVerificatorPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = RuVerificatorId()
    _create_contract = RuVerificatorCreateContract
    _response_contract = RuVerificatorResponseContract

