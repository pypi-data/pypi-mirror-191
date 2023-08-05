# di-ioc

Inversion of control / dependency injection for python

## TODO:

- [ ] Add AbstractLifetime class for singleton and scoped lifetimes
- [ ] Use ServiceRequest as the key to retrieve a service instead of just a type
  - This would change AbstractServiceProvider, AbstractServiceContainer, ServiceFactory
    to accept a ServiceRequest object that defines what service needs to be returned. It
    still allows for retrieving based on a type, but also allows for more complex resolving
    needs.
  - Maybe add a Resolver layer inside the ServiceProvider that takes the request and ChainMap
    of service factories to resolve the requested service. It could be customized by user if
    needed.
