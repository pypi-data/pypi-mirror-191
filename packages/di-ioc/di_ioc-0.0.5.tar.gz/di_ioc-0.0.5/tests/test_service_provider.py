from dataclasses import dataclass

import pytest

from di_ioc import ServiceContainer, MissingServiceError, auto
from di_ioc.abstraction import BasicRequest


@dataclass
class MyService:
    value: int


class UnregisteredService:
    pass


@pytest.fixture()
def realistic_container() -> ServiceContainer:
    container = ServiceContainer()
    container[MyService] = lambda t, s: MyService(123)

    child_container = ServiceContainer()
    child_container[MyService] = lambda t, s: MyService(456)

    container.register(child_container)

    return container


def test_get_optional_service(realistic_container: ServiceContainer):
    assert realistic_container.get_service(UnregisteredService) is None


def test_get_required_service(realistic_container: ServiceContainer):
    with pytest.raises(MissingServiceError):
        realistic_container.get_required_service(UnregisteredService)


def test_get_multiple_services(realistic_container: ServiceContainer):
    [service1, service2] = realistic_container.get_services(MyService)
    assert service1.value == 123
    assert service2.value == 456


def test_get_multiple_missing_services(realistic_container: ServiceContainer):
    assert realistic_container.get_services(UnregisteredService) == []


def test_request_with_arg_override():
    container = ServiceContainer()
    container[MyService] = auto(MyService)
    req = BasicRequest(MyService, args={'value': 1})
    service = container.get_required_service(req)
    assert service.value == 1
