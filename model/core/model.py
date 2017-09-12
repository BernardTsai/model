#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODOS:
# - better comments and docs
# - tests, tests, tests
# -  check seperators of links "-" maybe replace with = and exclude = from names
# - get_interface delivers None - how to resolve if a false network has been used in xref (=> better validation?)
#
# - better validate IP settings
#
# - better validation messages
#

# ------------------------------------------------------------------------------
#
# model.py:
#
# ------------------------------------------------------------------------------

from validate import Validate
from render   import Render
from input    import Input
from output   import Output

# ------------------------------------------------------------------------------
#
# Class Model
#
# ------------------------------------------------------------------------------
class Model(Validate,Input,Render,Output):

    # --------------------------------------------------------------------------
    version = "V0.0.1"

    # --------------------------------------------------------------------------
    def __init__(self,context="default"):
        """Initialize model """

        self.model = self._get_default_model(context)

    # --------------------------------------------------------------------------
    def set(self, data):
        # validate data structure
        self.validate( data )

        # increment version
        self.model["version"] = self.model["version"] + 1

        # determine type of data
        type = data["type"]

        if type == "VNF":
            self.set_vnf( data )
        elif type == "Tenant":
            self.set_tenant( data )
        elif type == "ExternalNetwork":
            self.set_external_network( data )
        elif type == "InternalNetwork":
                self.set_internal_network( data )
        elif type == "ExternalComponent":
            self.set_external_component( data )
        elif type == "InternalComponent":
            self.set_internal_component( data )
        elif type == "Node":
            self.set_node( data )

    # --------------------------------------------------------------------------
    def set_external_network(self, data):
        # determine name
        name  = data["name"]
        state = data["state"]

        networks = self.model["networks"]
        network = self._get( networks, "/" + name )
        if not network:
            network = self._get_default_external_network( name )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( networks, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","target","state"]:
            self._replace( network, data, attr )

        if "ipv4" in data:
            for attr in ["cidr","network","length","gateway","dns","dhcp","start","end","broadcast"]:
                self._replace( network["ipv4"], data["ipv4"], attr )

        if "ipv6" in data:
            for attr in ["cidr","network","length","gateway","dns","dhcp","start","end","broadcast"]:
                self._replace( network["ipv6"], data["ipv6"], attr )

        self._set( networks, network )

        self._set_references()

    # --------------------------------------------------------------------------
    def set_external_component(self, data):
        # determine name
        name  = data["name"]
        state = data["state"]

        components = self.model["components"]
        component = self._get( components, "/" + name )
        if not component:
            component = self._get_default_external_component( name )

        # check if the network has been defined
        networks = self.model["networks"]
        network = self._get( networks, data["network"] )
        if not network:
            raise AttributeError( "Invalid network name" )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( components, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","network","state","ipv4","ipv6","requirements","capabilities"]:
            self._replace( component, data, attr )

        self._set( components, component )

        self._set_references()

        # TODO: propagate state if required to all attached interfaces

    # --------------------------------------------------------------------------
    def set_vnf(self, data):
        # determine vnf and state
        name  = data["name"]
        state = data["state"]

        vnfs = self.model["vnfs"]
        vnf = self._get( vnfs, "/" + name )
        if not vnf:
            vnf = self._get_default_vnf( name )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( vnfs, name )
            return

        # update the attributes
        for attr in ["description","version","vendor","state"]:
            self._replace( vnf, data, attr )

        self._set( vnfs, vnf )

        # propagate the state
        for tenant in vnf["tenants"]:
            self._set_tenant_state( tenant, state )

        self._set_references()

    # --------------------------------------------------------------------------
    def set_tenant(self, data):
        # determine vnf and state
        vnf_name = data["vnf"]
        name     = data["name"]
        state    = data["state"]

        vnfs = self.model["vnfs"]
        vnf = self._get( vnfs, "/" + vnf_name )
        if not vnf:
            raise AttributeError( "Invalid VNF name" )

        tenants = vnf["tenants"]
        tenant = self._get( tenants, "/" + vnf_name + "/" + name )
        if not tenant:
            tenant = self._get_default_tenant( vnf_name, name )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( tenants, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","vnf","datacenter","state"]:
            self._replace( tenant, data, attr )

        self._set( tenants, tenant )

        # propagate the state
        for component in tenant["components"]:
            self._set_component_state( component, state )

        self._set_references()

    # --------------------------------------------------------------------------
    def set_internal_network(self, data):
        # determine vnf, tenant, name and state
        vnf_name    = data["vnf"]
        tenant_name = data["tenant"]
        name        = data["name"]
        state       = data["state"]

        vnfs = self.model["vnfs"]
        vnf = self._get( vnfs, "/" + vnf_name )
        if not vnf:
            raise AttributeError( "Invalid VNF name" )

        tenants = vnf["tenants"]
        tenant = self._get( tenants, "/" + vnf_name + "/" + tenant_name )
        if not tenant:
            raise AttributeError( "Invalid tenant name" )

        networks = tenant["networks"]
        network = self._get( networks, "/" + vnf_name + "/" + tenant_name + "/" + name )
        if not network:
            network = self._get_default_internal_network( vnf_name, tenant_name, name )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( networks, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","state"]:
            self._replace( network, data, attr )

        if "ipv4" in data:
            for attr in ["cidr","network","length","gateway","dns","dhcp","start","end","broadcast"]:
                self._replace( network["ipv4"], data["ipv4"], attr )

        if "ipv6" in data:
            for attr in ["cidr","network","length","gateway","dns","dhcp","start","end","broadcast"]:
                self._replace( network["ipv6"], data["ipv6"], attr )

        self._set( networks, network )

        self._set_references()

    # --------------------------------------------------------------------------
    def set_internal_component(self, data):
        # determine vnf, tenant, name and state
        vnf_name    = data["vnf"]
        tenant_name = data["tenant"]
        name        = data["name"]
        state       = data["state"]

        vnfs = self.model["vnfs"]
        vnf = self._get( vnfs, "/" + vnf_name )
        if not vnf:
            raise AttributeError( "Invalid VNF name" )

        tenants = vnf["tenants"]
        tenant = self._get( tenants, "/" + vnf_name + "/" + tenant_name )
        if not tenant:
            raise AttributeError( "Invalid tenant name" )

        components = tenant["components"]
        component = self._get( components, "/" + vnf_name + "/" + tenant_name + "/" + name )
        if not component:
            component = self._get_default_internal_component( vnf_name, tenant_name, name )

        # check if the network has been defined
        networks = self.model["networks"] + tenant["networks"]
        for capability in data["capabilities"]:
            network = self._get( networks, capability["network"] )
            if not network:
                raise AttributeError( "Invalid network name" )
        for requirement in data["requirements"]:
            network = self._get( networks, requirement["network"] )
            if not network:
                raise AttributeError( "Invalid network name" )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( components, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","placement",
                     "flavor","image","minimum_size","maximum_size","default_size",
                     "user_data","metadata","state","volumes","interfaces","requirements","capabilities"]:
            self._replace( component, data, attr )

        for interface in component["interfaces"]:
            interface["rules"] = []

        self._set( components, component )

        # adjust nodes
        nodes = component["nodes"]
        nr_nodes = len( nodes )
        if nr_nodes == 0:
            nr_nodes = component["default_size"]
        elif nr_nodes < component["minimum_size"]:
            nr_nodes = component["minimum_size"]
        elif component["maximum_size"] < nr_nodes:
            nr_nodes = component["maximum_size"]
        nodes = []

        for index in range(nr_nodes):
            node = self._get_default_node( vnf_name, tenant_name, name, index )

            # update the attributes
            for attr in ["description","version","placement",
                         "flavor","image","minimum_size","maximum_size","default_size",
                         "user_data","metadata","state","volumes","interfaces","requirements","capabilities"]:
                self._replace( node, data, attr )

            for interface in node["interfaces"]:
                interface["rules"] = []

            self._set( nodes, node )

        component["nodes"] = nodes

        self._set_references()

        # TODO: propagate state if required to all attached interfaces

    # --------------------------------------------------------------------------
    def set_node(self, data):
        # determine vnf, tenant, component, name and state
        vnf_name       = data["vnf"]
        tenant_name    = data["tenant"]
        component_name = data["component"]
        name           = data["name"]
        state          = data["state"]

        vnfs = self.model["vnfs"]
        vnf = self._get( vnfs, "/" + vnf_name )
        if not vnf:
            raise AttributeError( "Invalid VNF name" )

        tenants = vnf["tenants"]
        tenant = self._get( tenants, "/" + vnf_name + "/" + tenant_name )
        if not tenant:
            raise AttributeError( "Invalid tenant name" )

        components = tenant["components"]
        component = self._get( components, "/" + vnf_name + "/" + tenant_name + "/" + component_name )
        if not component:
            raise AttributeError( "Invalid component name" )

        nodes = component["nodes"]
        node = self._get( nodes, "/" + vnf_name + "/" + tenant_name + "[" + str(name) + "]" )
        new_node = False
        if not node:
            new_node = True
            node = self._get_default_node( vnf_name, tenant_name, component_name, name )

        # check if the change fits into the cluster dimensions
        current_size = len( nodes )
        new_size     = current_size
        if new_node and state != "undefined":
            new_size = current_size + 1
            if component["maximum_size"] < new_size:
                raise AttributeError( "Too many nodes" )
        elif not new_node and state == "undefined":
            new_size = current_size + 1
            if new_size < component["minimum_size"]:
                raise AttributeError( "Too few nodes" )

        # check if the vnf needs to be undefined
        if state == "undefined":
            self._remove( nodes, name )
            self._set_references()
            return

        # update the attributes
        for attr in ["description","version","placement","flavor","image",
                     "user_data","metadata","state","volumes","interfaces","requirements","capabilities"]:
            self._replace( node, data, attr )

        for interface in node["interfaces"]:
            interface["rules"] = []

        self._set( nodes, node )

        self._set_references()

        # TODO: propagate state if required to all attached interfaces

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    def _set_tenant_state(self, tenant, state):
        tenant["state"] = state

        # propagate the state
        for network in tenant["networks"]:
            self._set_network_state( network, state )
        for component in tenant["components"]:
            self._set_component_state( component, state )

    # --------------------------------------------------------------------------
    def _set_network_state(self, network, state):
        network["state"] = state

    # --------------------------------------------------------------------------
    def _set_component_state(self, component, state):
        component["state"] = state

        # propagate the state
        for node in component["nodes"]:
            self._set_node_state( node, state )

    # --------------------------------------------------------------------------
    def _set_node_state(self, node, state):
        node["state"] = state

        # propagate the state
        for volume in node["volumes"]:
            self._set_volume_state( volume, state )
        for interface in node["interface"]:
            self._set_interace_state( interface, state )

    # --------------------------------------------------------------------------
    def _set_volume_state(self, volume, state):
        volume["state"] = state

    # --------------------------------------------------------------------------
    def _set_interface_state(self, interface, state):
        interface["state"] = state

    # --------------------------------------------------------------------------
    def _get_default_model(self,context):
        model = {
            "type":        "Model",
            "context":     context,
            "version":     0,
            "vnfs":        [],
            "networks":    [],
            "components":  [],
            "consistent":  True
        }

        return model

    # --------------------------------------------------------------------------
    def _get_default_external_network(self,name):
        network = {
            "uuid":        "/" + name,
            "type":        "ExternalNetwork",
            "name":        name,
            "description": "",
            "version":     "0.0.0",
            "state":       "defined",
            "target":      "",
            "ipv4":
            {
                "cidr":      "192.168.178.0/24",
                "network":   "192.168.178.0",
                "length":    "24",
                "gateway":   "192.168.178.1",
                "dns":       "192.168.178.2",
                "dhcp":      "192.168.178.3",
                "start":     "192.168.178.128",
                "end":       "192.168.178.253",
                "broadcast": "192.168.178.254"
            },
            "ipv6":
            {
                "cidr":      "fd00::/8",
                "network":   "fd00::",
                "length":    "8",
                "gateway":   "fd00::01",
                "dns":       "fd00::02",
                "dhcp":      "fd00::03",
                "start":     "fd00::80",
                "end":       "fd00::fd",
                "broadcast": "fd00::ff"
            }
        }

        return network

    # --------------------------------------------------------------------------
    def _get_default_internal_network(self,vnf,tenant,name):
        network = {
            "uuid":        "/" + vnf + "/" + tenant + "/" + name,
            "type":        "Network",
            "name":        name,
            "description": "",
            "version":     "0.0.0",
            "vnf":         vnf,
            "tenant":      tenant,
            "state":       "defined",
            "ipv4":
            {
                "cidr":      "192.168.178.0/24",
                "network":   "192.168.178.0",
                "length":    "24",
                "gateway":   "192.168.178.1",
                "dns":       "192.168.178.2",
                "dhcp":      "192.168.178.3",
                "start":     "192.168.178.128",
                "end":       "192.168.178.253",
                "broadcast": "192.168.178.254"
            },
            "ipv6":
            {
                "cidr":      "fd00::/8",
                "network":   "fd00::",
                "length":    "8",
                "gateway":   "fd00::01",
                "dns":       "fd00::02",
                "dhcp":      "fd00::03",
                "start":     "fd00::80",
                "end":       "fd00::fd",
                "broadcast": "fd00::ff"
            }
        }

        return network

    # --------------------------------------------------------------------------
    def _get_default_external_component(self,name):
        component = {
            "uuid":         "/" + name,
            "type":         "ExternalComponent",
            "name":         name,
            "description":  "",
            "version":      "0.0.0",
            "state":        "defined",
            "network":      "",
            "ipv4":         [],
            "ipv6":         [],
            "requirements": [],
            "capabilities": []
        }

        return component

    # --------------------------------------------------------------------------
    def _get_default_internal_component(self,vnf,tenant,name):
        component = {
            "uuid":         "/" + vnf + "/" + tenant + "/" + name,
            "type":         "InternalComponent",
            "name":         name,
            "description":  "",
            "version":      "0.0.0",
            "vnf":          vnf,
            "tenant":       tenant,
            "state":        "defined",
            "placement":    "EXT",
            "flavor":       "undefined",
            "image":        "undefined",
            "minimum_size": 1,
            "maximum_size": 1,
            "default_size": 1,
            "user_data":    [],
            "metadata":     [],
            "nodes":        [],
            "volumes":      [],
            "interfaces":   [],
            "requirements": [],
            "capabilities": []
        }

        return component

    # --------------------------------------------------------------------------
    def _get_default_vnf(self, name):
        vnf = {
            "uuid":         "/" + name,
            "type":        "VNF",
            "name":        name,
            "description": "",
            "version":     "0.0.0",
            "vendor":      "undefined",
            "state":       "defined",
            "tenants":     [],
            "networks":    [],
            "partners":    []
        }

        return vnf

    # --------------------------------------------------------------------------
    def _get_default_tenant(self,vnf,name):
        tenant = {
            "uuid":         "/" + vnf + "/" + name,
            "type":        "Tenant",
            "name":        name,
            "description": "",
            "version":     "0.0.0",
            "vnf":         vnf,
            "state":       "defined",
            "components":  [],
            "networks":    []
        }

        return tenant

    # --------------------------------------------------------------------------
    def _get_default_node(self,vnf,tenant,component,name):
        node = {
            "uuid":         "/" + vnf + "/" + tenant + "/" + component + "[" + str(name) + "]",
            "type":         "Node",
            "name":         name,
            "description":  "",
            "version":      "0.0.0",
            "vnf":          vnf,
            "tenant":       tenant,
            "component":    component,
            "state":        "defined",
            "placement":    "EXT",
            "flavor":       "undefined",
            "image":        "undefined",
            "user_data":    [],
            "metadata":     [],
            "nodes":        [],
            "volumes":      [],
            "interfaces":   [],
            "requirements": [],
            "capabilities": []
        }

        return node

    # --------------------------------------------------------------------------
    def _set_references(self):
        networks     = self._get_networks()
        components   = self._get_components()
        capabilities = self._get_capabilities(components)
        links        = self._get_links(components,capabilities)

        self._set_rules(networks,components,links)

    # --------------------------------------------------------------------------
    def _get_networks(self):
        networks = self.model["networks"]

        for vnf in self.model["vnfs"]:
            for tenant in vnf["tenants"]:
                networks = networks + tenant["networks"]

        return networks

    # --------------------------------------------------------------------------
    def _get_components(self):
        components = self.model["components"]

        vnfs = self.model["vnfs"]
        for vnf in vnfs:
            tenants = vnf["tenants"]
            for tenant in tenants:
                components = components + tenant["components"]

        return components

    # --------------------------------------------------------------------------
    def _get_capabilities(self,components):
        capabilities = dict()
        for component in components:
            for capability in component["capabilities"]:
                if component["type"] == "ExternalComponent":
                    network  = component["network"]
                    external = True
                else:
                    network  = capability["network"]
                    external = False

                name  = component["uuid"] + "-" + capability["name"]

                capabilities[ name ] = {
                    "name":       name,
                    "component":  component["uuid"],
                    "capability": capability["name"],
                    "network":    network,
                    "endpoints":  capability["endpoints"],
                    "external":   external
                }

        return capabilities

    # --------------------------------------------------------------------------
    def _get_links(self,components,capabilities):
        links = []

        self.model["consistent"] = True

        for component in components:
            for requirement in component["requirements"]:

                # find capability
                capability_name = requirement["component"] + '-' + requirement["capability"]

                # not found
                if not capability_name in capabilities:
                    self.model["consistent"] = False
                    continue

                # found
                capability      = capabilities[ capability_name ]

                # add new link
                name = component["uuid"] + '-' + capability["name"]

                if component["type"] == "ExternalComponent":
                    network  = component["network"]
                    external = True
                else:
                    network  = requirement["network"]
                    external = False

                link = {
                    'name':              name,
                    "capability":        capability["capability"],
                    'endpoints':         capability["endpoints"],
                    "source_component":  component["uuid"],
                    "source_network":    network,
                    "source_external":   external,
                    "target_component":  capability["component"],
                    "target_network":    capability["network"],
                    "target_external":   capability["external"]
                }

                links.append(link)

        return links

    # --------------------------------------------------------------------------
    def _get_interface(self,component,network):
        for interface in component["interfaces"]:
            if interface["network"] == network["uuid"]:
                return interface
        return None

    # --------------------------------------------------------------------------
    def _get_network(self,networks,uuid):
        for network in networks:
            if network["uuid"] == uuid:
                return network
        return None

    # --------------------------------------------------------------------------
    def _get_component(self,components,uuid):
        for component in components:
            if component["uuid"] == uuid:
                return component
        return None

    # --------------------------------------------------------------------------
    def _clear_rules(self,components):
        for component in components:
            if component["type"] == "InternalComponent":
                for interface in component["interfaces"]:
                    interface["rules"] = []
                for node in component["nodes"]:
                    for interface in node["interfaces"]:
                        interface["rules"] = []

    # --------------------------------------------------------------------------
    def _set_rules(self,networks,components,links):

        # remove all existing rules first
        self._clear_rules(components)

        # loop over all links and calculate rules
        for link in links:

            # determine source and target networks and components
            source_network   = self._get_network( networks,     link["source_network"]   )
            target_network   = self._get_network( networks,     link["target_network"]   )
            source_component = self._get_component( components, link["source_component"] )
            target_component = self._get_component( components, link["target_component"] )
            endpoints        = link["endpoints"]

            # ----- egress rules for internal source components -----
            if not link["source_external"]:
                interface = self._get_interface(source_component,source_network)

                # external targets
                if link["target_external"]:
                    for endpoint in endpoints:
                        for prefix in target_component["ipv4"]:
                            rule = {
                                "direction": "egress",
                                "mode":      "cidr",
                                "group":     link["target_component"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv4",
                                "prefix":    prefix
                            }
                            interface["rules"].append(rule)
                        for prefix in target_component["ipv6"]:
                            rule = {
                                "direction": "egress",
                                "mode":      "cidr",
                                "group":     link["target_component"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv6",
                                "prefix":    prefix
                            }
                            interface["rules"].append(rule)
                # internal targets
                else:
                    if "ipv4" in target_network:
                        for endpoint in endpoints:
                            rule = {
                                "direction": "egress",
                                "mode":      "group",
                                "group":     link["target_component"] + "_" + link["target_network"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv4",
                                "prefix":    target_network["ipv4"]["cidr"]
                            }
                            interface["rules"].append(rule)
                    if "ipv6" in target_network:
                        for endpoint in endpoints:
                            rule = {
                                "direction": "egress",
                                "mode":      "group",
                                "group":     link["target_component"] + "_" + link["target_network"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv6",
                                "prefix":    target_network["ipv6"]["cidr"]
                            }
                            interface["rules"].append(rule)

            # ----- ingress rules for internal target components -----
            if not link["target_external"]:
                interface = self._get_interface(target_component, target_network)

                # external sources
                if link["source_external"]:
                    for endpoint in endpoints:
                        for prefix in source_component["ipv4"]:
                            rule = {
                                "direction": "ingress",
                                "mode":      "cidr",
                                "group":     link["source_component"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv4",
                                "prefix":    prefix
                            }
                            interface["rules"].append(rule)
                        for prefix in source_component["ipv6"]:
                            rule = {
                                "direction": "ingress",
                                "mode":      "cidr",
                                "group":     link["source_component"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv6",
                                "prefix":    prefix
                            }
                            interface["rules"].append(rule)
                # internal sources
                else:
                    if "ipv4" in source_network:
                        for endpoint in endpoints:
                            rule = {
                                "direction": "ingress",
                                "mode":      "group",
                                "group":     link["source_component"] + "_" + link["source_network"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv4",
                                "prefix":    target_network["ipv4"]["cidr"]
                            }
                            interface["rules"].append(rule)
                    if "ipv6" in target_network:
                        for endpoint in endpoints:
                            rule = {
                                "direction": "egress",
                                "mode":      "group",
                                "group":     link["source_component"] + "_" + link["source_network"],
                                "protocol":  endpoint["protocol"],
                                "port_min":  endpoint["port_min"],
                                "port_max":  endpoint["port_max"],
                                "family":    "IPv6",
                                "prefix":    target_network["ipv6"]["cidr"]
                            }
                            interface["rules"].append(rule)

        # apply component interface rules to node interfaces
        for component in components:
            if component["type"] == "InternalComponent":
                for index, interface in enumerate(component["interfaces"]):
                    for node in component["nodes"]:
                        node["interfaces"][index]["rules"] = interface["rules"]

    # --------------------------------------------------------------------------
    def _get(self,list,uuid):
        for item in list:
            if item["uuid"] == uuid:
                return item
        return None

    # --------------------------------------------------------------------------
    def _set(self,list,new_item):
        name = new_item["name"]

        for index, item in enumerate(list):
            if item["name"] == name:
                list[index] = new_item
                return

        list.append( new_item )

    # --------------------------------------------------------------------------
    def _remove(self,list,name):
        for index, item in enumerate(list):
            if item["name"] == name:
                del list[index]
                return

    # --------------------------------------------------------------------------
    def _replace(self,object1,object2,name):
        if name in object2:
            object1[name] = object2[name]

# ------------------------------------------------------------------------------
