import inspect
import typing
from typing import Callable, Type, Generic, List, Iterable

from .abstraction import TService, ServiceFactory, AbstractServiceProvider, AbstractServiceRequest, BasicRequest

ServiceCtor = Callable[[...], TService]


class DepResolver(Generic[TService]):
    def __init__(self, param_name: str, service_type: Type[TService], fallback: TService | None = None, required=True,
                 find_all=False):
        self.param_name = param_name
        self.service_type = service_type
        self.fallback = fallback
        self.required = required
        self.find_all = find_all

    def __call__(self, req: AbstractServiceRequest, sp: AbstractServiceProvider):
        if isinstance(req, BasicRequest) and self.param_name in req.arg_overrides:
            return req.arg_overrides[self.param_name]

        if self.find_all:
            return sp.get_services(self.service_type)

        if self.required:
            return sp.get_required_service(self.service_type)

        return sp.get_service(self.service_type) or self.fallback


class DerivedServiceFactory(Generic[TService], ServiceFactory[TService]):
    """
    Attempts to automatically derive a service factory from a callable using the type annotations in
    its signature.

    If a type annotation has more than one service type possibility, the first type is used.

    :param ctor: function that accepts dependencies for a service which can be resolved from a service provider
                 and returns an instance of the service.
    :return: a service factory that can be registered with a container.
    """

    def __init__(self, ctor: ServiceCtor[TService]):
        self.ctor = ctor
        self.dep_resolvers: List[DepResolver] = []

        for i, p in enumerate(inspect.signature(ctor).parameters.values()):
            if i == 0 and p.name == 'self':
                raise ValueError(f'the service constructor is not allowed to be an instance method.')

            if p.annotation is None:
                raise _param_error(p.name, ctor.__name__, 'does not have a type annotation')

            if p.default != inspect.Parameter.empty:
                # has default
                self.dep_resolvers.append(DepResolver(p.name, p.annotation, p.default, False))
            elif type(None) in typing.get_args(p.annotation):
                # optional
                type_args = list(typing.get_args(p.annotation))
                type_args.remove(type(None))
                if len(type_args) == 0:
                    raise _param_error(p.name, ctor.__name__, 'has an optional type annotation that is None')
                self.dep_resolvers.append(DepResolver(p.name, type_args[0], None, False))
            else:
                # required
                type_origin = typing.get_origin(p.annotation)
                if inspect.isclass(type_origin) and issubclass(type_origin, (List, Iterable)):
                    type_args = typing.get_args(p.annotation)
                    if len(type_args) == 0:
                        raise _param_error(p.name, ctor.__name__, 'has a list/iterable type annotation without an valid'
                                                                  'element type')
                    self.dep_resolvers.append(DepResolver(p.name, type_args[0], find_all=True))
                else:
                    self.dep_resolvers.append(DepResolver(p.name, p.annotation))

    def __call__(self, req: AbstractServiceRequest[TService], sp: AbstractServiceProvider) -> TService:
        return self.ctor(
            *(f(req, sp)
              for f in self.dep_resolvers))


def _param_error(name: str, ctor_name: str, reason: str):
    return TypeError(f'failed to create auto service factory because parameter {name} of '
                     f'{ctor_name} {reason}.')


def auto(ctor: ServiceCtor, lifetime=None) -> ServiceFactory:
    """
    Automatically derive a ServiceFactory for the service constructor.
    :param ctor: callable which creates the service. Can be a function or class, which uses the __init__ method.
    :param lifetime: optional lifetime (singleton, scoped). Default is None (transient)
    :return:
    """
    factory = DerivedServiceFactory(ctor)
    if lifetime:
        factory = lifetime(factory)
    return factory
