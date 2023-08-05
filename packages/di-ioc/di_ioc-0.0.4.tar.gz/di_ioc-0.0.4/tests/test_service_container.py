from di_ioc import ServiceContainer, singleton


class AbstractService1:
    pass


class AbstractService2:
    pass


class MyService(AbstractService1, AbstractService2):
    pass


def test_register_multiple_services():
    container = ServiceContainer()

    factory = singleton(lambda *_: MyService())
    container[[AbstractService1, AbstractService2]] = factory

    assert container[AbstractService1] == [factory]
    assert container[AbstractService2] == [factory]

    assert container.get_required_service(AbstractService1) == container.get_required_service(AbstractService2)
