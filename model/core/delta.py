#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# delta.py:
#
# A class to provide functionality for calculating the difference between models.
#
# ------------------------------------------------------------------------------
# TODO:
# - adding networks, components etc. under tenants is not reflected in delta list
# ------------------------------------------------------------------------------

import yaml

# ------------------------------------------------------------------------------
#
# Class Delta
#
# ------------------------------------------------------------------------------
class Delta():

    # --------------------------------------------------------------------------
    def __init__(self, model1, model2):
        """Initialize delta"""

        # save references to models and the diff
        self.model1 = model1
        self.model2 = model2
        self.tree1  = model1.getModel()
        self.tree2  = model2.getModel()
        self.model  = {
            "schema":     self.model1.getSchema(),
            "context":    self.tree1["context"],
            "version1":   self.tree1["version"],
            "version2":   self.tree2["version"],
            "networks":   [],
            "components": [],
            "vnfs":       []
        }

        # create indexes for both models
        self.index1 = self._create_index( self.tree1 )
        self.index2 = self._create_index( self.tree2 )

        # difference between external networks
        networks  = self.model["networks"]
        networks1 = self.tree1["networks"]
        networks2 = self.tree2["networks"]
        self._delta_entities( networks, networks1, networks2 )

        # difference between external components
        components  = self.model["components"]
        components1 = self.tree1["components"]
        components2 = self.tree2["components"]
        self._delta_entities( components, components1, components2 )

        # difference between VNFs
        vnfs  = self.model["vnfs"]
        vnfs1 = self.tree1["vnfs"]
        vnfs2 = self.tree2["vnfs"]
        self._delta_entities( vnfs, vnfs1, vnfs2 )

        # difference between child elements of VNFs
        for vnf in vnfs:

            if vnf["action"] == "keep" or vnf["action"] == "change":
                vnf["tenants"] = []

                uuid = vnf["type"] + ":" + vnf["uuid"]
                vnf1 = self.index1[uuid]
                vnf2 = self.index2[uuid]

                tenants  = vnf["tenants"]
                tenants1 = vnf1["tenants"]
                tenants2 = vnf2["tenants"]
                self._delta_entities( tenants, tenants1, tenants2 )

                # difference between child elements of tenants
                for tenant in tenants:

                    if tenant["action"] == "keep" or tenant["action"] == "change":
                        tenant["networks"]   = []
                        tenant["components"] = []

                        uuid    = tenant["type"] + ":" + tenant["uuid"]
                        tenant1 = self.index1[uuid]
                        tenant2 = self.index2[uuid]

                        networks  = tenant["networks"]
                        networks1 = tenant1["networks"]
                        networks2 = tenant2["networks"]
                        self._delta_entities( networks, networks1, networks2 )

                        # difference between external components
                        components  = tenant["components"]
                        components1 = tenant1["components"]
                        components2 = tenant2["components"]
                        self._delta_entities( components, components1, components2 )

                        # difference between child elements of tenants
                        for component in components:
                            if component["action"] == "keep" or component["action"] == "change":
                                component["nodes"] = []

                                uuid       = component["type"] + ":" + component["uuid"]
                                component1 = self.index1[uuid]
                                component2 = self.index2[uuid]

                                nodes  = component["nodes"]
                                nodes1 = component1["nodes"]
                                nodes2 = component2["nodes"]
                                self._delta_entities( nodes, nodes1, nodes2 )

        # sort arrays in diff
        self.model["networks"]   = sorted( self.model["networks"],   key=self._action)
        self.model["components"] = sorted( self.model["components"], key=self._action)
        self.model["vnfs"]       = sorted( self.model["vnfs"],       key=self._action)

        for vnf in self.model["vnfs"]:
            vnf["tenants"] = sorted( vnf["tenants"], key=self._action)

            for tenant in vnf["tenants"]:
                tenant["networks"]   = sorted( tenant["networks"],   key=self._action)
                tenant["components"] = sorted( tenant["components"], key=self._action)

                for component in tenant["components"]:
                    component["nodes"] = sorted( component["nodes"], key=self._action)

    # --------------------------------------------------------------------------
    def getModel(self):
        """Provide model object"""
        return self.model

    # --------------------------------------------------------------------------
    def getModel1(self):
        """Provide first model object"""
        return self.model1

    # --------------------------------------------------------------------------
    def getModel2(self):
        """Provide second model object"""
        return self.model2

    # --------------------------------------------------------------------------
    def _action(self, item):
        if item["action"] == "remove":
            return 1
        if item["action"] == "keep":
            return 2
        if item["action"] == "change":
            return 3
        if item["action"] == "add":
            return 4

    # --------------------------------------------------------------------------
    def _create_index(self, model ):
        index = {}

        for network in model["networks"]:
            index["ExternalNetwork:" + network["uuid"]] = network

        for component in model["components"]:
            index["ExternalComponent:" + component["uuid"]] = component

        for vnf in model["vnfs"]:
            index["VNF:" + vnf["uuid"]] = vnf

            for tenant in vnf["tenants"]:
                index["Tenant:" + tenant["uuid"]] = tenant

                for network in tenant["networks"]:
                    index["InternalNetwork:" + network["uuid"]] = network

                for component in tenant["components"]:
                    index["InternalComponent:" + component["uuid"]] = component

                    for node in component["nodes"]:
                        index["Node:" + node["uuid"]] = node

        return index

    # --------------------------------------------------------------------------
    def _delta_entities(self, list, list1, list2 ):

        # delta between two lists of entities
        for item1 in list1:
            type1 = item1["type"]
            uuid1 = item1["uuid"]
            uuid  = type1 + ":" + uuid1
            if not uuid in self.index2:
                entity = { "type": type1, "uuid": uuid1, "action": "remove" }
                self._delta_subentities( entity, self.index1[uuid] )
                list.append( entity )
            else:
                item2 = self.index2[uuid]
                if type1 == "ExternalNetwork":
                    difference = (item1!=item2)
                elif type1 == "ExternalComponent":
                    difference = (item1!=item2)
                elif type1 == "VNF":
                    difference = self._delta_vnf( item1, item2 )
                elif type1 == "Tenant":
                    difference = self._delta_tenant( item1, item2 )
                elif type1 == "InternalNetwork":
                    difference = (item1!=item2)
                elif type1 == "InternalComponent":
                    difference = self._delta_internal_component( item1, item2 )
                elif type1 == "Node":
                    difference = (item1!=item2)

                if difference:
                    list.append( { "type": type1, "uuid": uuid1, "action": "change" } )
                else:
                    list.append( { "type": type1, "uuid": uuid1, "action": "keep" } )

        for item2 in list2:
            type2 = item2["type"]
            uuid2 = item2["uuid"]
            uuid  = type2 + ":" + uuid2
            if not uuid in self.index1:
                entity = { "type": type2, "uuid": uuid2, "action": "add" }
                self._delta_subentities( entity, self.index2[uuid] )
                list.append( entity )

    # --------------------------------------------------------------------------
    def _delta_subentities(self, entity, element ):
        action = entity["action"]
        type   = entity["type"]

        # cascade action to all subelements of a VNF
        if type == "VNF":
            entity["tenants"] = []
            for tenant in element["tenants"]:
                subentity = { "type": "Tenant", "uuid": tenant["uuid"], "action": action }
                entity["tenants"].append( subentity )
                self._delta_subentities( subentity, tenant)

        # cascade action to all subelements of a tenant
        elif type == "Tenant":
            entity["networks"]   = []
            entity["components"] = []
            for network in element["networks"]:
                subentity = { "type": "InternalNetwork", "uuid": network["uuid"], "action": action }
                entity["networks"].append( subentity )

            for component in element["components"]:
                subentity = { "type": "InternalComponent", "uuid": component["uuid"], "action": action }
                entity["components"].append( subentity )
                self._delta_subentities( subentity, component)

        # cascade action to all subelements of a component
        elif type == "InternalComponent":
            entity["nodes"] = []
            for node in element["nodes"]:
                subentity = { "type": "Node", "uuid": node["uuid"], "action": action }
                entity["nodes"].append( subentity )

    # --------------------------------------------------------------------------
    def _delta_vnf(self, vnf1, vnf2 ):
        for attr in ["description","version","vendor","state"]:
            if vnf1[attr] != vnf2[attr]:
                return True

    # --------------------------------------------------------------------------
    def _delta_tenant(self, tenant1, tenant2 ):
        for attr in ["description","version","vnf","datacenter","state"]:
            if tenant1[attr] != tenant2[attr]:
                return True

    # --------------------------------------------------------------------------
    def _delta_internal_component(self, component1, component2 ):
        for attr in ["description","version","placement",
                     "flavor","image","minimum_size","maximum_size","default_size",
                     "user_data","metadata","state","volumes","interfaces","requirements","capabilities"]:
            if component1[attr] != component2[attr]:
                return True
