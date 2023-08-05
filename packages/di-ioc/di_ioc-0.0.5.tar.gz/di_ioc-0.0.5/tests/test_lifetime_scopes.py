from di_ioc import ServiceContainer, singleton, scoped, auto


class MyService:
    pass


def test_singleton():
    container = ServiceContainer()
    container[MyService] = singleton(lambda t, s: MyService())
    assert container.get_service(MyService) == container.get_service(MyService)


def test_scoped():
    container = ServiceContainer()
    container[MyService] = auto(MyService, lifetime=scoped)
    with container.create_scope() as scope1:
        assert scope1.get_service(MyService) != container.get_service(MyService)
