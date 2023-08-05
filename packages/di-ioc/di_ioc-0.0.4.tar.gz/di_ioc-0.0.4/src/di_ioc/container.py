import logging
from typing import Type, Optional, Mapping, Iterator, ChainMap, Self, List, Sequence, Iterable, Protocol

from .abstraction import AbstractServiceContainer, AbstractServiceProvider, ServiceFactory, TService, \
    MissingServiceError, Request, BasicRequest, AbstractServiceRequest
from .scope import ServiceScope

log = logging.getLogger(__name__)


class Resolver(Protocol):

    @staticmethod
    def resolve(req: AbstractServiceRequest,
                services: Mapping[Type, List[ServiceFactory]]) -> Optional[ServiceFactory]:
        f = services.get(req.service_type)
        return f[0] if f else None

    @staticmethod
    def resolve_all(req: AbstractServiceRequest,
                    services: Mapping[Type, List[ServiceFactory]]) -> Sequence[ServiceFactory]:
        factories = []
        search_stack = [services]

        while len(search_stack):
            mapping = search_stack.pop()
            if isinstance(mapping, ChainMap):
                search_stack.extend(reversed(mapping.maps))
            elif isinstance(mapping, ServiceContainer):
                factories.extend(Resolver.resolve_all(req, mapping._registry))
            else:
                factories.extend(mapping.get(req.service_type, []))

        return factories


class DefaultResolver(Resolver):
    pass


class ServiceContainer(AbstractServiceContainer, AbstractServiceProvider, ServiceScope):

    def __init__(self, *factories: Mapping[Type, List[ServiceFactory]],
                 resolver: Resolver = None):
        super().__init__()
        self._registry = ChainMap[Type, List[ServiceFactory]]({}, *factories)
        self._resolver: Resolver = resolver or DefaultResolver()

    def __hash__(self) -> int:
        return id(self)

    def __getitem__(self, service_type: Type[TService]) -> Sequence[ServiceFactory[TService]]:
        return self._registry[service_type]

    def __setitem__(self, service_type: Type | Iterable[Type], service_factory: ServiceFactory) -> None:
        head = self._registry.maps[0]
        if isinstance(service_type, Sequence):
            for t in service_type:
                self._add_factory(head, t, service_factory)
        else:
            self._add_factory(head, service_type, service_factory)

    def __delitem__(self, service_type: Type) -> None:
        del self._registry[service_type]

    def __len__(self) -> int:
        return len(self._registry)

    def __iter__(self) -> Iterator[Type]:
        return iter(self._registry)

    def __enter__(self) -> Self:
        log.debug('entered service scope')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
        log.debug('exited service scope')

    def get_service(self, request: Request[TService]) -> Optional[TService]:
        if not isinstance(request, AbstractServiceRequest):
            request = BasicRequest(request)

        if issubclass(request.service_type, AbstractServiceProvider):
            return self.create_scope()

        service_factory = self._resolver.resolve(request, self._registry)
        return service_factory(request, self) if service_factory else None

    def get_required_service(self, request: Request[TService]) -> TService:
        service = self.get_service(request)
        if service is None:
            raise MissingServiceError(request)
        return service

    def get_services(self, request: Request[TService]) -> List[TService]:
        if not isinstance(request, AbstractServiceRequest):
            request = BasicRequest(request)

        if issubclass(request.service_type, AbstractServiceProvider):
            return [self.create_scope()]

        factories = self._resolver.resolve_all(request, self._registry)
        return [f(request, self) for f in factories]

    def register(self, *other: AbstractServiceContainer):
        self._registry.maps.extend(other)

    def create_scope(self) -> Self:
        return ServiceContainer(self._registry)

    @staticmethod
    def _add_factory(map, key, factory: ServiceFactory):
        if not (factories := map.get(key)):
            factories = []
            map[key] = factories
        factories.append(factory)
