from typing import TypeVar, Generic

from di_ioc import ServiceContainer

T = TypeVar('T')


class GenericService(Generic[T]):
    def __init__(self, value: T):
        self.value = value


def test_can_use_parameterized_service_type():
    container = ServiceContainer()
    container[[GenericService, GenericService[int]]] = lambda *_: GenericService[int](0)
    container[[GenericService, GenericService[str]]] = lambda *_: GenericService[str]('hello')
    int_service = container.get_service(GenericService[int])
    str_service = container.get_service(GenericService[str])

    assert int_service.value == 0
    assert str_service.value == 'hello'
