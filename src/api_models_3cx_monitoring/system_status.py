from dataclasses import dataclass
from typing import List, Union, Any, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class status:
    fqdn: str
    web_meeting_fqdn: str
    web_meeting_status: int
    version: str
    recording_state: int
    activated: bool
    max_sim_calls: int
    max_sim_meeting_participants: int
    call_history_count: int
    chat_messages_count: int
    extensions_registered: int
    own_push: bool
    ip: str
    ip_v4: str
    ip_v6: str
    local_ip_valid: bool
    current_local_ip: str
    available_local_ips: str
    extensions_total: int
    has_unregistered_system_extensions: bool
    has_not_running_services: bool
    trunks_registered: int
    trunks_total: int
    calls_active: int
    blacklisted_ip_count: int
    memory_usage: int
    physical_memory_usage: int
    free_virtual_memory: int
    total_virtual_memory: int
    free_physical_memory: int
    total_physical_memory: int
    disk_usage: int
    free_disk_space: int
    total_disk_space: int
    cpu_usage: int
    cpu_usage_history: List[List[Union[datetime, float]]]
    maintenance_expires_at: datetime
    support: bool
    license_active: bool
    expiration_date: datetime
    outbound_rules: int
    backup_scheduled: bool
    last_backup_date_time: datetime
    reseller_name: str
    license_key: str
    product_code: str
    is_audit_log_enabled: bool
    is_spla: bool

    @staticmethod
    def from_dict(obj: Any) -> 'status':
        assert isinstance(obj, dict)
        fqdn = from_str(obj.get("FQDN"))
        web_meeting_fqdn = from_str(obj.get("WebMeetingFQDN"))
        web_meeting_status = int(from_str(obj.get("WebMeetingStatus")))
        version = from_str(obj.get("Version"))
        recording_state = from_int(obj.get("RecordingState"))
        activated = from_bool(obj.get("Activated"))
        max_sim_calls = from_int(obj.get("MaxSimCalls"))
        max_sim_meeting_participants = from_int(obj.get("MaxSimMeetingParticipants"))
        call_history_count = from_int(obj.get("CallHistoryCount"))
        chat_messages_count = from_int(obj.get("ChatMessagesCount"))
        extensions_registered = from_int(obj.get("ExtensionsRegistered"))
        own_push = from_bool(obj.get("OwnPush"))
        ip = from_str(obj.get("Ip"))
        ip_v4 = from_str(obj.get("IpV4"))
        ip_v6 = from_str(obj.get("IpV6"))
        local_ip_valid = from_bool(obj.get("LocalIpValid"))
        current_local_ip = from_str(obj.get("CurrentLocalIp"))
        available_local_ips = from_str(obj.get("AvailableLocalIps"))
        extensions_total = from_int(obj.get("ExtensionsTotal"))
        has_unregistered_system_extensions = from_bool(obj.get("HasUnregisteredSystemExtensions"))
        has_not_running_services = from_bool(obj.get("HasNotRunningServices"))
        trunks_registered = from_int(obj.get("TrunksRegistered"))
        trunks_total = from_int(obj.get("TrunksTotal"))
        calls_active = from_int(obj.get("CallsActive"))
        blacklisted_ip_count = from_int(obj.get("BlacklistedIpCount"))
        memory_usage = from_int(obj.get("MemoryUsage"))
        physical_memory_usage = from_int(obj.get("PhysicalMemoryUsage"))
        free_virtual_memory = from_int(obj.get("FreeVirtualMemory"))
        total_virtual_memory = from_int(obj.get("TotalVirtualMemory"))
        free_physical_memory = from_int(obj.get("FreePhysicalMemory"))
        total_physical_memory = from_int(obj.get("TotalPhysicalMemory"))
        disk_usage = from_int(obj.get("DiskUsage"))
        free_disk_space = from_int(obj.get("FreeDiskSpace"))
        total_disk_space = from_int(obj.get("TotalDiskSpace"))
        cpu_usage = from_int(obj.get("CpuUsage"))
        cpu_usage_history = from_list(lambda x: from_list(lambda x: from_union([from_float, from_datetime], x), x), obj.get("CpuUsageHistory"))
        maintenance_expires_at = from_datetime(obj.get("MaintenanceExpiresAt"))
        support = from_bool(obj.get("Support"))
        license_active = from_bool(obj.get("LicenseActive"))
        expiration_date = from_datetime(obj.get("ExpirationDate"))
        outbound_rules = from_int(obj.get("OutboundRules"))
        backup_scheduled = from_bool(obj.get("BackupScheduled"))
        last_backup_date_time = from_datetime(obj.get("LastBackupDateTime"))
        reseller_name = from_str(obj.get("ResellerName"))
        license_key = from_str(obj.get("LicenseKey"))
        product_code = from_str(obj.get("ProductCode"))
        is_audit_log_enabled = from_bool(obj.get("IsAuditLogEnabled"))
        is_spla = from_bool(obj.get("IsSpla"))
        return status(fqdn, web_meeting_fqdn, web_meeting_status, version, recording_state, activated, max_sim_calls, max_sim_meeting_participants, call_history_count, chat_messages_count, extensions_registered, own_push, ip, ip_v4, ip_v6, local_ip_valid, current_local_ip, available_local_ips, extensions_total, has_unregistered_system_extensions, has_not_running_services, trunks_registered, trunks_total, calls_active, blacklisted_ip_count, memory_usage, physical_memory_usage, free_virtual_memory, total_virtual_memory, free_physical_memory, total_physical_memory, disk_usage, free_disk_space, total_disk_space, cpu_usage, cpu_usage_history, maintenance_expires_at, support, license_active, expiration_date, outbound_rules, backup_scheduled, last_backup_date_time, reseller_name, license_key, product_code, is_audit_log_enabled, is_spla)

    def to_dict(self) -> dict:
        result: dict = {}
        result["FQDN"] = from_str(self.fqdn)
        result["WebMeetingFQDN"] = from_str(self.web_meeting_fqdn)
        result["WebMeetingStatus"] = from_str(str(self.web_meeting_status))
        result["Version"] = from_str(self.version)
        result["RecordingState"] = from_int(self.recording_state)
        result["Activated"] = from_bool(self.activated)
        result["MaxSimCalls"] = from_int(self.max_sim_calls)
        result["MaxSimMeetingParticipants"] = from_int(self.max_sim_meeting_participants)
        result["CallHistoryCount"] = from_int(self.call_history_count)
        result["ChatMessagesCount"] = from_int(self.chat_messages_count)
        result["ExtensionsRegistered"] = from_int(self.extensions_registered)
        result["OwnPush"] = from_bool(self.own_push)
        result["Ip"] = from_str(self.ip)
        result["IpV4"] = from_str(self.ip_v4)
        result["IpV6"] = from_str(self.ip_v6)
        result["LocalIpValid"] = from_bool(self.local_ip_valid)
        result["CurrentLocalIp"] = from_str(self.current_local_ip)
        result["AvailableLocalIps"] = from_str(self.available_local_ips)
        result["ExtensionsTotal"] = from_int(self.extensions_total)
        result["HasUnregisteredSystemExtensions"] = from_bool(self.has_unregistered_system_extensions)
        result["HasNotRunningServices"] = from_bool(self.has_not_running_services)
        result["TrunksRegistered"] = from_int(self.trunks_registered)
        result["TrunksTotal"] = from_int(self.trunks_total)
        result["CallsActive"] = from_int(self.calls_active)
        result["BlacklistedIpCount"] = from_int(self.blacklisted_ip_count)
        result["MemoryUsage"] = from_int(self.memory_usage)
        result["PhysicalMemoryUsage"] = from_int(self.physical_memory_usage)
        result["FreeVirtualMemory"] = from_int(self.free_virtual_memory)
        result["TotalVirtualMemory"] = from_int(self.total_virtual_memory)
        result["FreePhysicalMemory"] = from_int(self.free_physical_memory)
        result["TotalPhysicalMemory"] = from_int(self.total_physical_memory)
        result["DiskUsage"] = from_int(self.disk_usage)
        result["FreeDiskSpace"] = from_int(self.free_disk_space)
        result["TotalDiskSpace"] = from_int(self.total_disk_space)
        result["CpuUsage"] = from_int(self.cpu_usage)
        result["CpuUsageHistory"] = from_list(lambda x: from_list(lambda x: from_union([to_float, lambda x: x.isoformat()], x), x), self.cpu_usage_history)
        result["MaintenanceExpiresAt"] = self.maintenance_expires_at.isoformat()
        result["Support"] = from_bool(self.support)
        result["LicenseActive"] = from_bool(self.license_active)
        result["ExpirationDate"] = self.expiration_date.isoformat()
        result["OutboundRules"] = from_int(self.outbound_rules)
        result["BackupScheduled"] = from_bool(self.backup_scheduled)
        result["LastBackupDateTime"] = self.last_backup_date_time.isoformat()
        result["ResellerName"] = from_str(self.reseller_name)
        result["LicenseKey"] = from_str(self.license_key)
        result["ProductCode"] = from_str(self.product_code)
        result["IsAuditLogEnabled"] = from_bool(self.is_audit_log_enabled)
        result["IsSpla"] = from_bool(self.is_spla)
        return result


def welcome_from_dict_systemstatus(s: Any) -> status:
    return status.from_dict(s)


def welcome_to_dict_systemstatus(x: status) -> Any:
    return to_class(status, x)
