Installation
============

This document explains the basic steps in order to setup an environment
for making use of the orchestrator.

Prerequisites
-------------

* workstation with admin rights and internet access
* bash
* python 3.X
* git
* sshuttle
* favourite editor eg. vi, atom, ...
* access privileges to GitLab environment in Darmstadt
* access privileges to SOL OpenStack environment in Darmstadt

Installation
------------

* **Create and activate a virtual runtime environment on your workstation:**

```
> virtualenv -p python3 model
> cd model
> source bin/activate
```

* **Install OpenStack and Heat python clients and python shade library (for custom programs) and ansible:**

```bash
> pip install python-openstackclient
> pip install python-heatclient
> pip install shade
> pip install ansible
> pip install pyyaml
> pip install jsonschema
> pip install flask
```

* **Open ssh connection to the SOL environment:**

Ensure that a valid entry for the SOL jumphost has been defined in ~/.ssh/config

```
Host SOL_jumphost
    User           [your user name]
    Port           22
    HostName       80.146.205.203
    IdentityFile   [path to private key file]
    ForwardAgent   yes
    TcpKeepAlive   yes
```

Open ssh connection in the background:

```
> sshuttle -vNHr SOL_jumphost
```

* **Clone TOSCA generator:**

Clones the repository to the workstation, installs the additional required packages.
Initialises the submodule and the corresponding required packages.

```bash
> git clone https://github.com/BernardTsai/model.git
> cd model
> pip install -r requirements.txt
```
