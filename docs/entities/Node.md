Node
====

A node describes a compute node belonging to an internal component within a virtual datacenter.
Its name in combination with the name of the VNF, the name of the tenant and the name of the internal component to which it belongs uniquely identifies it within the context of a model.

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
component:    ...
placement:    ...
flavor:       ...
image:        ...
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

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **type**         | Node                                            |
| **name**         | unique integer                                  |
| description      | short description (max 2048 characters)         |
| **state**        | undefined, defined, inactive, active, failure   |
| **version**      | semantic version Vx.y.z                         |
| **vnf**          | name of VNF (4-256 characters)                  |
| **tenant**       | name of tenant (4-256 characters)               |
| **component**    | name of internal component (4-256 characters)   |
| **placement**    | EXT, INT or MGMT                                |
| **flavor**       | sizing of the compute nodes (string)            |
| **image**        | name of the OS image (string)                   |
| user_data        | list of user data strings                       |
| metadata         | list of metadata strings                        |
| volumes          | list of volume properties                       |
| interfaces       | list of interface properties                    |
| requirements     | list of requirement properties                  |
| capabilities     | list of capability properties                   |

_required properties are marked in bold_

Volume Properties
-----------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **device**       | device name (string)                            |
| **size**         | size of volume in GB (positive integer)         |
| **type**         | filesystem type (string)                        |
| **mount**        | mount point (string)                            |

_required properties are marked in bold_

Interface Properties
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

- **uuid**: `[VNF name]_[Tenant name]_[Component name]_[Node name]`
- **name**: a unique integer within context of an internal Component


Example
-------

```yaml
---
type:        Node
name:        1
description: A test cluster within the test tenant
version:     V0.1.0
state:       defined
vnf:         Test-VNF
tenant:      Test Tenant
component:   Test Cluster
placement:   EXT
flavor:      m1.medium
image:       Ubuntu-14.04
user_data:   ["ABCD"]
metadata:    ["XYZ"]
volumes:
  - device: "/dev/vdb"
    size:   100
    type:   ext4
    mount:  "/data"
interfaces:
  - network: public
    ipv4_fixed:
      - 192.168.178.10
      - 192.168.178.11
requirements: []
capabilities: []

```
