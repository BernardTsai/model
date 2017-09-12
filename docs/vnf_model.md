VNF Model
=========

The VNF model is an internal abstract hierarchical representation of a virtualized network function and the way it interacts with its external communication partners.

```yaml
model:
 ... global properties of the model ...
 ...
 networks:
  - ... properties of an external network ...
  - ...
 components:
  - ... properties of an external component ...
  - ...
 vnfs:   
  - ... properties of a VNF ...
    tenants:
      - ... properties of a tenant ...
        networks:
          - ... properties of an internal network ...
          - ...
        components:
          - ... properties of an internal component ...
          - ...
            nodes:
              - ... properties of a single node ...
              - ...
      - ...
  - ...
```

The model is created and changed by either applying target [state definitions](state_definitions.md) (SD) for entities of the virtualized network function or updating the state of individual entities based on monitoring state information (SI).

```
VNF Model V1 + SD/SI -> VNF Model V2
VNF Model V2 + SD/SI -> VNF Model V3
...
```

It needs to be mentioned that the internal model contains additional information which has been calculated from the entity specific property and state information it may have received. This information is derived with the help of algorithms reflecting: the mapping between abstract and actual deployment architecture, security considerations (e.g. security rules), etc. .

The orchestrator derives from the difference between different versions of the model the actions which it needs to apply in order to converge to the desired target state.


```
VNF Model V2 - VNF Model V1 -> Delta -> Actions
```

The information maintained in the VNF model can be used to render any kind of reports with the help of a templating mechanism.

Following types of entities are maintained in the VNF model:

| Entity Type                                         | Description                                                        |
|-----------------------------------------------------|--------------------------------------------------------------------|
| [External Network](entities/ExternalNetwork.md)     | Routing networks connecting the VNF services to the external world |
| [External Component](entities/ExternalComponent.md) | External communication partners                                    |
| [VNF](entities/VNF.md)                              | The virtualized network function itself                            |
| [Tenant](entities/Tenant.md)                        | A virtualized data center belonging to the VNF                     |
| [Internal Network](entities/InternalNetwork.md)     | A tenant routing network                                           |
| [Internal Component](entities/InternalComponent.md) | A cluster of compute nodes                                         |
| [Node]((entities/Node.md))                          | A single compute node                                              |
