Internal Network
=================

An internal network describes a tenant specific routing network.
Its name in combination with the name of the VNF and the name of the tenant uniquely identifies it within the context of a model.

The general structure:

```yaml
---
type:        ...
name:        ...
description: ...
state:       ...
version:     ...
vnf:         ...
tenant:      ...
ipv4:        ...
ipv6:        ...
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
| **vnf**          | name of the VNF (string)                        |
| **tenant**       | name of the tenant (string)                     |
| ipv4             | IPv4 properties                                 |
| ipv6             | IPv6 properties                                 |

_required properties are marked in bold_

IPv4 Properties
---------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **cidr**         | network CIDR (string)                           |
| network          | network address (string)                        |
| length           | length (integer between 0 and 32)               |
| gateway          | gateway address                                 |
| dns              | dns server address                              |
| dhcp             | dhcp server address                             |
| start            | start DHCP IP address                           |
| end              | end DHCP IP address                             |
| broadcast        | network broadcast address                       |

_required properties are marked in bold_

IPv6 Properties
---------------

| Property         | Description                                     |
|------------------|-------------------------------------------------|
| **cidr**         | network CIDR (string)                           |
| network          | network address (string)                        |
| length           | length (integer between 0 and 32)               |
| gateway          | gateway address                                 |
| dns              | dns server address                              |
| dhcp             | dhcp server address                             |
| start            | start DHCP IP address                           |
| end              | end DHCP IP address                             |
| broadcast        | network broadcast address                       |

_required properties are marked in bold_

Remarks
-------

- **uuid**: `[VNF name]_[Tenant name]_[Network name]`
- **name**: a unique name within the model context merely consisting of alphabetical characters and possibly digits with a length between 8 and 256 characters

Example
-------

```yaml
---
type:        InternalNetwork
name:        oam
description: An internal test network
vnf:         Test
tenant:      SiteA
version:     V0.1.0
state:       defined
ipv4:
  cidr:      "192.168.178.0/24"
  network:   "192.168.178.0"
  length:    24
  gateway:   "192.168.178.1"
  dns:       "192.168.178.2"
  dhcp:      "192.168.178.3"
  start:     "192.168.178.128"
  end:       "192.168.178.253"
  broadcast: "192.168.178.254"
ipv6:
  cidr:      "fd00::/8"
  network:   "fd00::"
  length:    8
  gateway:   "fd00::01"
  dns:       "fd00::02"
  dhcp:      "fd00::03"
  start:     "fd00::80"
  end:       "fd00::fd"
  broadcast: "fd00::ff"
```
