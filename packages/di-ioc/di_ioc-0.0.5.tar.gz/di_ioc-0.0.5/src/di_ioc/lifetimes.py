import inspect
from dataclasses import dataclass
from typing import Callable, Dict, Generator, \
    Any, Generic

from .abstraction import AbstractServiceProvider, ServiceFactory, ServiceFactoryGenerator, TService, AbstractLifetime, \
    AbstractServiceRequest
from .scope import ServiceScope


@dataclass
class ServiceInstance:
    value: Any

    def dispose(self):
        pass


@dataclass
class DisposableServiceInstance(ServiceInstance):
    def __init__(self, disposable: Generator):
        if not inspect.isgenerator(disposable):
            raise ValueError('expected a generator!')

        super().__init__(next(disposable))
        self._generator = disposable

    def dispose(self):
        try:
            next(self._generator)
        except StopIteration:
            pass
        except:
            raise


def create_service_instance(req: AbstractServiceRequest[TService], s: AbstractServiceProvider, f: Callable,
                            cleanup: Callable):
    x = f(req, s)
    if inspect.isgenerator(x):
        if isinstance(s, ServiceScope):
            s.on_dispose.append(cleanup)
        else:
            raise RuntimeError(
                'The service container does not support the scoping mechanism yet disposable services '
                'are being used!')

        return DisposableServiceInstance(x)
    else:
        return ServiceInstance(x)


class singleton(Generic[TService], AbstractLifetime, ServiceFactory[TService]):
    def __init__(self, f: ServiceFactory[TService] | ServiceFactoryGenerator[TService]):
        self.f = f
        self.instance: ServiceInstance | None = None

    def dispose(self, *args):
        if self.instance:
            self.instance.dispose()
            self.instance = None

    def __call__(self, req: AbstractServiceRequest[TService], s: AbstractServiceProvider):
        if self.instance is None:
            self.instance = create_service_instance(req, s, self.f, self.dispose)
        return self.instance.value

    def __repr__(self):
        return f'Singleton({self.f}, instance={self.instance})'


class scoped(Generic[TService], AbstractLifetime, ServiceFactory[TService]):
    def __init__(self, f: ServiceFactory[TService] | ServiceFactoryGenerator[TService]):
        self.f = f
        self.instances: Dict[Any, ServiceInstance] = {}

    def dispose(self, s: ServiceScope):
        if instance := self.instances.get(s):
            instance.dispose()
            del self.instances[s]

    def __call__(self, req: AbstractServiceRequest[TService], s: AbstractServiceProvider):
        if (instance := self.instances.get(s)) is None:
            instance = create_service_instance(req, s, self.f, self.dispose)
            self.instances[s] = instance

        return instance.value

    def __repr__(self):
        return f'Scoped({self.f}, instances={len(self.instances)})'
