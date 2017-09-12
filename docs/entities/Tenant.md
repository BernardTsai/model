Tenant
======

A tenant represents a virtual datacenter belonging to a virtualized network function.
Its name in combination with the name of the VNF to which it belongs
uniquely identifies it within the context of a model.

The general structure:

```yaml
---
type:        ...
name:        ...
description: ...
state:       ...
version:     ...
vnf:         ...
datacenter:  ...
```

General Properties
------------------

| Property        | Description                                     |
|-----------------|-------------------------------------------------|
| **type**        | Tenant                                          |
| **name**        | unique identifier (8-256 characters)            |
| description     | short description (max 2048 characters)         |
| **state**       | undefined, defined, inactive, active, failure   |
| **version**     | semantic version Vx.y.z                         |
| **vnf**         | name of VNF (8-256 characters)                  |
| **datacenter**  | name of the data center (8-256 characters)      |

_required properties are marked in bold_

Remarks
-------

- **uuid**: `[VNF name]_[Tenant name]`
- **name**: a unique name within the VNF context for each tenant merely consisting of alphabetical characters and possibly digits with a length between 8 and 256 characters
- **datacenter**: the name of the datacenter needs to match a name defined
in the list of available datacenters. This list is subject to change.

Example
-------

```yaml
---
type:        Tenant
name:        SiteA
description: A tenant of the test virtualized network function at SiteA
state:       defined
version:     V0.1.0
vnf:         Test
datacenter:  SiteA
```
