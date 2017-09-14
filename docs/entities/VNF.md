VNF
===

A VNF is a virtualized network function. Its name uniquely identifies it within the context of a model.

The general structure:

```yaml
---
type:        ...
name:        ...
description: ...
state:       ...
version:     ...
vendor:      ...
```

General Properties
------------------

| Property        | Description                                     |
|-----------------|-------------------------------------------------|
| **type**        | VNF                                             |
| **name**        | unique identifier (4-256 characters)            |
| description     | short description (max 2048 characters)         |
| **state**       | undefined, defined, inactive, active, failure   |
| **version**     | semantic version Vx.y.z                         |
| **vendor**      | name of vendor (4-256 characters)               |

_required properties are marked in bold_

Remarks
-------

- **uuid**: `[VNF name]`
- **name**: a unique name for each VNF merely consisting of alphabetical characters and possibly digits with a length between 8 and 256 characters

Example:
--------

```yaml
---
type: VNF
name: Test
description: A test virtualized network function
version: V0.1.0
vendor: ACME
state:  defined
```
