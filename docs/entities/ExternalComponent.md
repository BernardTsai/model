External Component
==================

An external component describes an external communication partner.
Its name uniquely identifies it within the context of a model.

The general structure:

```yaml
---
type:         ...
name:         ...
description:  ...
state:        ...
version:      ...
network:      ...
ipv4:
 -            ...
ipv6:
 -            ...
requirements:   
 -            ...
capabilities:   
 -            ...
```

General Properties
------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **type**         | InternalComponent                               |
| **name**         | unique identifier (4-256 characters)            |
| description      | short description (max 2048 characters)         |
| **state**        | undefined, defined, inactive, active, failure   |
| **version**      | semantic version Vx.y.z                         |
| **network**      | uuid of network (string)                        |
| ipv4             | list of IPv4 CIDRs (string)                     |
| ipv6             | list of IPv6 CIDRs (string)                     |
| requirements     | list of requirement properties                  |
| capabilities     | list of capability properties                   |

_required properties are marked in bold_

Requirement Properties
----------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **component**    | uuid of internal or external component (string) |
| **capability**   | name of capability (string)                     |
| **network**      | uuid of network (string)                        |

_required properties are marked in bold_

Capability Properties
---------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **name**         | name of capability (string)                     |
| **network**      | uuid of network (string)                        |
| **endpoints**    | list of endpoint properties                     |

_required properties are marked in bold_

Endpoint Properties
-------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **protocol**     | TCP, UDP, ...                                   |
| **port_min**     | integer between 1 and 65535                     |
| **port_max**     | integer between 1 and 65535                     |

_required properties are marked in bold_

Remarks
-------

- **uuid**: `[Component name]`
- **name**: a unique name within the model context merely consisting of alphabetical characters and possibly digits with a length between 4 and 256 characters

Example
-------

```yaml
---
type:        ExternalComponent
name:        Test Partner
description: An external communication partner
version:     V0.1.0
state:       defined
network:     public
ipv4:
  - 0.0.0.0/0
requirements:
  - component:  Test_SiteA_Cluster
    capability: ssh
capabilities: []
```
