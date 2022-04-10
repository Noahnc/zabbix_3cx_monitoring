from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ListElement:
    id: int
    number: int
    name: str
    host: str
    type: str
    sim_calls: int
    external_number: str
    is_registered: bool
    register_ok_time: str
    register_sent_time: str
    register_failed_time: str
    can_be_deleted: bool
    is_expired_provider_root_certificate: Optional[bool] = None
    expired_provider_root_certificate_date: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ListElement':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("Id")))
        number = int(from_str(obj.get("Number")))
        name = from_str(obj.get("Name"))
        host = from_str(obj.get("Host"))
        type = from_str(obj.get("Type"))
        sim_calls = int(from_str(obj.get("SimCalls")))
        external_number = from_str(obj.get("ExternalNumber"))
        is_registered = from_bool(obj.get("IsRegistered"))
        register_ok_time = from_str(obj.get("RegisterOkTime"))
        register_sent_time = from_str(obj.get("RegisterSentTime"))
        register_failed_time = from_str(obj.get("RegisterFailedTime"))
        can_be_deleted = from_bool(obj.get("CanBeDeleted"))
        is_expired_provider_root_certificate = from_union([from_bool, from_none], obj.get("IsExpiredProviderRootCertificate"))
        expired_provider_root_certificate_date = from_union([from_str, from_none], obj.get("ExpiredProviderRootCertificateDate"))
        return ListElement(id, number, name, host, type, sim_calls, external_number, is_registered, register_ok_time, register_sent_time, register_failed_time, can_be_deleted, is_expired_provider_root_certificate, expired_provider_root_certificate_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_str(str(self.id))
        result["Number"] = from_str(str(self.number))
        result["Name"] = from_str(self.name)
        result["Host"] = from_str(self.host)
        result["Type"] = from_str(self.type)
        result["SimCalls"] = from_str(str(self.sim_calls))
        result["ExternalNumber"] = from_str(self.external_number)
        result["IsRegistered"] = from_bool(self.is_registered)
        result["RegisterOkTime"] = from_str(self.register_ok_time)
        result["RegisterSentTime"] = from_str(self.register_sent_time)
        result["RegisterFailedTime"] = from_str(self.register_failed_time)
        result["CanBeDeleted"] = from_bool(self.can_be_deleted)
        result["IsExpiredProviderRootCertificate"] = from_union([from_bool, from_none], self.is_expired_provider_root_certificate)
        result["ExpiredProviderRootCertificateDate"] = from_union([from_str, from_none], self.expired_provider_root_certificate_date)
        return result


@dataclass
class trunks:
    list: List[ListElement]
    is_refresh_trunks_registration_prohibited: bool
    is_licence_standard: bool

    @staticmethod
    def from_dict(obj: Any) -> 'trunks':
        assert isinstance(obj, dict)
        list = from_list(ListElement.from_dict, obj.get("list"))
        is_refresh_trunks_registration_prohibited = from_bool(obj.get("isRefreshTrunksRegistrationProhibited"))
        is_licence_standard = from_bool(obj.get("isLicenceStandard"))
        return trunks(list, is_refresh_trunks_registration_prohibited, is_licence_standard)

    def to_dict(self) -> dict:
        result: dict = {}
        result["list"] = from_list(lambda x: to_class(ListElement, x), self.list)
        result["isRefreshTrunksRegistrationProhibited"] = from_bool(self.is_refresh_trunks_registration_prohibited)
        result["isLicenceStandard"] = from_bool(self.is_licence_standard)
        return result


def welcome_from_dict_trunks(s: Any) -> trunks:
    return trunks.from_dict(s)


def welcome_to_dict_trunks(x: trunks) -> Any:
    return to_class(trunks, x)
