Internal Component
==================

An internal component describes a cluster of compute nodes residing within a virtual datacenter.
Its name in combination with the name of the VNF and the name of the tenant to which it belongs uniquely identifies it within the context of a model.

The general structure:

```yaml
---
type:         ...
name:         ...
description:  ...
state:        ...
version:      ...
vnf:          ...
tenant:       ...
placement:    ...
flavor:       ...
image:        ...
minimum_size: ...
maximum_size: ...
default_size: ...
user_data:
 -            ...
metadata:
 -            ...
volumes:
 -            ...
interfaces:   
 -            ...
requirements:   
 -            ...
capabilities:   
 -            ...
```

General Properties
------------------

| Property           | Description                                     |
|--------------------|-------------------------------------------------|
| **type**           | InternalComponent                               |
| **name**           | unique identifier (4-256 characters)            |
| description        | short description (max 2048 characters)         |
| **state**          | undefined, defined, inactive, active, failure   |
| **version**        | semantic version Vx.y.z                         |
| **vnf**            | name of VNF (4-256 characters)                  |
| **tenant**         | name of tenant (4-256 characters)               |
| **placement**      | EXT, INT or MGMT                                |
| **flavor**         | sizing of the compute nodes (string)            |
| **image**          | name of the OS image (string)                   |
| **minimum_size**   | min. size of cluster (positive integer)         |
| **maximum_size**   | max. size of cluster (positive integer)         |
| **default_size**   | def. size of cluster (positive integer)         |
| user_data          | list of user data strings                       |
| metadata           | list of metadata strings                        |
| [volumes](#1)      | list of volume properties                       |
| [interfaces](#2)   | list of interface properties                    |
| [requirements](#3) | list of requirement properties                  |
| [capabilities](#4) | list of capability properties                   |

_required properties are marked in bold_

Volume Properties<a name="1"></a>
-----------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **device**       | device name (string)                            |
| **size**         | size of volume in GB (positive integer)         |
| **type**         | filesystem type (string)                        |
| **mount**        | mount point (string)                            |

_required properties are marked in bold_

Interface Properties<a name="2"></a>
--------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **network**      | uuid of network (string)                        |
| type             | left, right, mgmt                               |
| ipv4_fixed       | list of IPv4 addresses (string)                 |
| ipv4_allowed     | list of IPv4 addresses (string)                 |
| ipv6_fixed       | list of IPv6 addresses (string)                 |
| ipv6_allowed     | list of IPv6 addresses (string)                 |

_required properties are marked in bold_

Requirement Properties<a name="3"></a>
----------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **component**    | uuid of internal or external component (string) |
| **capability**   | name of capability (string)                     |
| **network**      | uuid of network (string)                        |

_required properties are marked in bold_

Capability Properties<a name="4"></a>
---------------------

| Property            | Description                                     |
|---------------------|-------------------------------------------------|
| **name**            | name of capability (string)                     |
| **network**         | uuid of network (string)                        |
| [**endpoints**](#5) | list of endpoint properties                     |

_required properties are marked in bold_

Endpoint Properties<a name="5"></a>
-------------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **protocol**     | TCP, UDP, ...                                   |
| **port_min**     | integer between 1 and 65535                     |
| **port_max**     | integer between 1 and 65535                     |

_required properties are marked in bold_

Remarks
-------

- **uuid**: `[VNF name]_[Tenant name]_[Component name]`
- **name**: a unique name within tenant context merely consisting of alphabetical characters and possibly digits with a length between 4 and 256 characters


Example
-------

```yaml
---
type:         InternalComponent
name:         Cluster
description:  A test cluster within the test tenant
state:        defined
version:      V0.1.0
vnf:          Test
tenant:       SiteA
placement:    EXT
flavor:       m1.medium
image:        Ubuntu-14.04
minimum_size: 3
maximum_size: 5
default_size: 3
user_data:    ["ABC"]
metadata:     ["XYZ"]
volumes:
  - device: "/dev/vdb"
    size:   100
    type:   ext4
    mount:  "/data"
interfaces:
  - network: "/Test Network"
    ipv4_fixed:
      - 192.168.178.10
      - 192.168.178.11
requirements: []
capabilities:
  - name:    ssh
    network: /Test Network
    endpoints:
      - protocol: TCP
        port_min: 22
        port_max: 22
```
