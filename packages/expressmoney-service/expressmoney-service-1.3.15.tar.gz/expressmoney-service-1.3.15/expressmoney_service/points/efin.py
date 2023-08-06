__all__ = ('EfinILOrderPoint', 'EfinCancelOrderPoint', 'EfinFailOrderPoint', 'EfinSuccessOrderPoint')

from phonenumber_field.serializerfields import PhoneNumberField

from ..api import *

_SERVICE = 'services'


class _EfinILOrderCreateContract(Contract):
    product_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    city = serializers.CharField(max_length=32)
    address = serializers.CharField(max_length=250)
    phonenumber = PhoneNumberField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    meeting_day = serializers.DateField()


class _EfinILOrderReadContract(Contract):
    created = serializers.DateTimeField()
    meeting_day = serializers.DateField()
    sign_day = serializers.DateField(allow_null=True)
    status_code = serializers.IntegerField()
    status_name = serializers.CharField(max_length=150)
    status_description = serializers.CharField(max_length=256)
    status_date = serializers.DateTimeField(allow_null=True)


class _EfinCancelOrderCreateContract(Contract):
    pass


class EfinSuccessCreateContract(Contract):
    efin_il_order_id = serializers.IntegerField()


class EfinFailCreateContract(Contract):
    efin_il_order_id = serializers.IntegerField()
    payload = serializers.JSONField()


class _EfinILOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'efin_il_order'


class _EfinCancelOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'set_canceled'


class _EfinSuccessOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'efin_success'


class _EfinFailOrder(ID):
    _service = _SERVICE
    _app = 'efin'
    _view_set = 'efin_fail'


class EfinILOrderPoint(CreatePointMixin, ListPointMixin, ContractPoint):
    _point_id = _EfinILOrder()
    _create_contract = _EfinILOrderCreateContract
    _read_contract = _EfinILOrderReadContract
    _sort_by = 'created'


class EfinCancelOrderPoint(CreatePointMixin, ContractPoint):
    _point_id = _EfinCancelOrder()
    _create_contract = _EfinCancelOrderCreateContract


class EfinSuccessOrderPoint(CreatePointMixin, ContractPoint):
    _point_id = _EfinSuccessOrder()
    _create_contract = EfinSuccessCreateContract


class EfinFailOrderPoint(CreatePointMixin, ContractPoint):
    _point_id = _EfinFailOrder()
    _create_contract = EfinFailCreateContract
