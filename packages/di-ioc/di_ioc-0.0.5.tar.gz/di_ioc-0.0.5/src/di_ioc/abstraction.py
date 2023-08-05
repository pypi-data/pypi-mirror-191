from abc import ABC, abstractmethod
from typing import Callable, Type, TypeVar, Optional, ContextManager, Generator, \
    Hashable, Self, MutableMapping, List, Mapping, Iterable, Generic, Any

TService = TypeVar('TService')


class MissingServiceError(Exception):
    def __init__(self, service_type: Type):
        self.service_type = service_type
        super().__init__()


class AbstractServiceRequest(Generic[TService]):
    @property
    @abstractmethod
    def service_type(self) -> Type[TService]:
        """
        The requested service_type
        :return:
        """


class BasicRequest(Generic[TService], AbstractServiceRequest[TService]):

    def __init__(self, service_type: Type[TService], args: Mapping[str, Any] = None):
        self._service_type = service_type
        self._args: Mapping[str, Any] = args or {}

    @property
    def service_type(self) -> Type[TService]:
        return self._service_type

    @property
    def arg_overrides(self) -> Mapping[str, Any]:
        return self._args


Request = Type[TService] | AbstractServiceRequest[TService]


class AbstractServiceProvider(Hashable, ContextManager[Self], ABC):
    @abstractmethod
    def get_service(self, request: Request[TService]) -> Optional[TService]:
        """
        Try to get a service instance if it exists.
        :param request:
        :return: the service instance or None.
        """

    @abstractmethod
    def get_required_service(self, request: Request[TService]) -> TService:
        """
        Get a service instance or fail with an exception.
        :param request:
        :return: the service instance.
        :raises MissingServiceError: there is not a service registered under the service_type.
        """

    @abstractmethod
    def get_services(self, request: Request[TService]) -> List[TService]:
        """
        Produce a list of all services that satisfy the service_type.
        :param request:
        :return: list of all service instances that match the service_type.
        """

    @abstractmethod
    def create_scope(self) -> Self:
        """
        Create a new provider that inherits all the service factories and
        causes scoped factories to produce a new instance. Singleton factories
        will return the same instance the parent provider does.
        :return:
        """


DisposableServiceInstance = Generator[TService, None, None]
ServiceFactory = Callable[[AbstractServiceRequest[TService], AbstractServiceProvider], TService]
ServiceFactoryGenerator = Callable[
    [AbstractServiceRequest[TService], AbstractServiceProvider],
    DisposableServiceInstance[TService]]


class AbstractServiceContainer(MutableMapping[Type | Iterable[Type], ServiceFactory],
                               Mapping[Type, List[ServiceFactory]],
                               ABC):

    @abstractmethod
    def register(self, *other: 'AbstractServiceContainer'):
        """
        'Mount' other service containers into this one and make their services available from this one. Each mounted
        container is still distinct from this one.
        :param other:
        :return:
        """


class AbstractScope(ABC):
    @abstractmethod
    def dispose(self) -> None:
        """
        Cleanup everything that needs disposed in this scope.
        :return:
        """


class AbstractLifetime(ABC):

    @abstractmethod
    def dispose(self, scope: AbstractScope) -> None:
        """
        Cleanup at the end of lifetime.
        :return:
        """
