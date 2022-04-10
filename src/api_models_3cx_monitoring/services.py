from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class service:
    name: str
    display_name: str
    status: int
    memory_used: int
    cpu_usage: int
    thread_count: int
    handle_count: int
    start_stop_enabled: bool
    restart_enabled: bool

    @staticmethod
    def from_dict(obj: Any) -> 'service':
        assert isinstance(obj, dict)
        name = from_str(obj.get("Name"))
        display_name = from_str(obj.get("DisplayName"))
        status = from_int(obj.get("Status"))
        memory_used = from_int(obj.get("MemoryUsed"))
        cpu_usage = from_int(obj.get("CpuUsage"))
        thread_count = from_int(obj.get("ThreadCount"))
        handle_count = from_int(obj.get("HandleCount"))
        start_stop_enabled = from_bool(obj.get("startStopEnabled"))
        restart_enabled = from_bool(obj.get("restartEnabled"))
        return service(name, display_name, status, memory_used, cpu_usage, thread_count, handle_count, start_stop_enabled, restart_enabled)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.name)
        result["DisplayName"] = from_str(self.display_name)
        result["Status"] = from_int(self.status)
        result["MemoryUsed"] = from_int(self.memory_used)
        result["CpuUsage"] = from_int(self.cpu_usage)
        result["ThreadCount"] = from_int(self.thread_count)
        result["HandleCount"] = from_int(self.handle_count)
        result["startStopEnabled"] = from_bool(self.start_stop_enabled)
        result["restartEnabled"] = from_bool(self.restart_enabled)
        return result


def welcome_from_dict_services(s: Any) -> List[service]:
    return from_list(service.from_dict, s)


def welcome_to_dict_services(x: List[service]) -> Any:
    return from_list(lambda x: to_class(service, x), x)
