# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Status:
    status: bool
    time: str
    agents: int
    calls: int

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        status = from_bool(obj.get("Status"))
        time = from_str(obj.get("Time"))
        agents = int(from_str(obj.get("Agents")))
        calls = from_int(obj.get("Calls"))
        return Status(status, time, agents, calls)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Status"] = from_bool(self.status)
        result["Time"] = from_str(self.time)
        result["Agents"] = from_str(str(self.agents))
        result["Calls"] = from_int(self.calls)
        return result


@dataclass
class ListElement:
    id: str
    number: str
    name: str
    host: str
    type: str
    sim_calls: int
    external_number: str
    register_ok_time: str
    register_sent_time: str
    register_failed_time: str
    can_be_deleted: bool
    is_registered: Optional[bool] = None
    is_expired_provider_root_certificate: Optional[bool] = None
    expired_provider_root_certificate_date: Optional[str] = None
    audio_port: Optional[int] = None
    log_file_size: Optional[int] = None
    security: Optional[int] = None
    log_level: Optional[int] = None
    passive_server_is_enabled: Optional[bool] = None
    passive_server: Optional[str] = None
    sbc_id: Optional[int] = None
    password: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    provision_link: Optional[str] = None
    public_ip: Optional[str] = None
    local_ip: Optional[str] = None
    version: Optional[str] = None
    secure: Optional[bool] = None
    os: Optional[str] = None
    out_of_date: Optional[bool] = None
    status: Optional[Status] = None
    legacy: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ListElement':
        assert isinstance(obj, dict)
        id = from_str(obj.get("Id"))
        number = from_str(obj.get("Number"))
        name = from_str(obj.get("Name"))
        host = from_str(obj.get("Host"))
        type = from_str(obj.get("Type"))
        sim_calls = from_union([from_int, lambda x: int(from_str(x))], obj.get("SimCalls"))
        external_number = from_str(obj.get("ExternalNumber"))
        register_ok_time = from_str(obj.get("RegisterOkTime"))
        register_sent_time = from_str(obj.get("RegisterSentTime"))
        register_failed_time = from_str(obj.get("RegisterFailedTime"))
        can_be_deleted = from_bool(obj.get("CanBeDeleted"))
        is_registered = from_union([from_bool, from_none], obj.get("IsRegistered"))
        is_expired_provider_root_certificate = from_union([from_bool, from_none], obj.get("IsExpiredProviderRootCertificate"))
        expired_provider_root_certificate_date = from_union([from_str, from_none], obj.get("ExpiredProviderRootCertificateDate"))
        audio_port = from_union([from_int, from_none], obj.get("AudioPort"))
        log_file_size = from_union([from_int, from_none], obj.get("LogFileSize"))
        security = from_union([from_int, from_none], obj.get("Security"))
        log_level = from_union([from_int, from_none], obj.get("LogLevel"))
        passive_server_is_enabled = from_union([from_bool, from_none], obj.get("PassiveServerIsEnabled"))
        passive_server = from_union([from_str, from_none], obj.get("PassiveServer"))
        sbc_id = from_union([from_int, from_none], obj.get("SbcId"))
        password = from_union([from_str, from_none], obj.get("Password"))
        description = from_union([from_str, from_none], obj.get("Description"))
        link = from_union([from_str, from_none], obj.get("Link"))
        provision_link = from_union([from_str, from_none], obj.get("ProvisionLink"))
        public_ip = from_union([from_str, from_none], obj.get("PublicIP"))
        local_ip = from_union([from_str, from_none], obj.get("LocalIP"))
        version = from_union([from_str, from_none], obj.get("Version"))
        secure = from_union([from_bool, from_none], obj.get("Secure"))
        os = from_union([from_str, from_none], obj.get("OS"))
        out_of_date = from_union([from_bool, from_none], obj.get("OutOfDate"))
        status = from_union([Status.from_dict, from_none], obj.get("Status"))
        legacy = from_union([from_bool, from_none], obj.get("Legacy"))
        return ListElement(id, number, name, host, type, sim_calls, external_number, register_ok_time, register_sent_time, register_failed_time, can_be_deleted, is_registered, is_expired_provider_root_certificate, expired_provider_root_certificate_date, audio_port, log_file_size, security, log_level, passive_server_is_enabled, passive_server, sbc_id, password, description, link, provision_link, public_ip, local_ip, version, secure, os, out_of_date, status, legacy)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_str(self.id)
        result["Number"] = from_str(self.number)
        result["Name"] = from_str(self.name)
        result["Host"] = from_str(self.host)
        result["Type"] = from_str(self.type)
        result["SimCalls"] = from_int(self.sim_calls)
        result["ExternalNumber"] = from_str(self.external_number)
        result["RegisterOkTime"] = from_str(self.register_ok_time)
        result["RegisterSentTime"] = from_str(self.register_sent_time)
        result["RegisterFailedTime"] = from_str(self.register_failed_time)
        result["CanBeDeleted"] = from_bool(self.can_be_deleted)
        result["IsRegistered"] = from_union([from_bool, from_none], self.is_registered)
        result["IsExpiredProviderRootCertificate"] = from_union([from_bool, from_none], self.is_expired_provider_root_certificate)
        result["ExpiredProviderRootCertificateDate"] = from_union([from_str, from_none], self.expired_provider_root_certificate_date)
        result["AudioPort"] = from_union([from_int, from_none], self.audio_port)
        result["LogFileSize"] = from_union([from_int, from_none], self.log_file_size)
        result["Security"] = from_union([from_int, from_none], self.security)
        result["LogLevel"] = from_union([from_int, from_none], self.log_level)
        result["PassiveServerIsEnabled"] = from_union([from_bool, from_none], self.passive_server_is_enabled)
        result["PassiveServer"] = from_union([from_str, from_none], self.passive_server)
        result["SbcId"] = from_union([from_int, from_none], self.sbc_id)
        result["Password"] = from_union([from_str, from_none], self.password)
        result["Description"] = from_union([from_str, from_none], self.description)
        result["Link"] = from_union([from_str, from_none], self.link)
        result["ProvisionLink"] = from_union([from_str, from_none], self.provision_link)
        result["PublicIP"] = from_union([from_str, from_none], self.public_ip)
        result["LocalIP"] = from_union([from_str, from_none], self.local_ip)
        result["Version"] = from_union([from_str, from_none], self.version)
        result["Secure"] = from_union([from_bool, from_none], self.secure)
        result["OS"] = from_union([from_str, from_none], self.os)
        result["OutOfDate"] = from_union([from_bool, from_none], self.out_of_date)
        result["Status"] = from_union([lambda x: to_class(Status, x), from_none], self.status)
        result["Legacy"] = from_union([from_bool, from_none], self.legacy)
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


def welcome_from_dict_trunk(s: Any) -> trunks:
    return trunks.from_dict(s)


def welcome_to_dict_trunk(x: trunks) -> Any:
    return to_class(trunks, x)
