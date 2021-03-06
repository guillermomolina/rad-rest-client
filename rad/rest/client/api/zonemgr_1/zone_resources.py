# Copyright 2021, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from rad.rest.client import RADException
from rad.rest.client.api.resource import Resource
from rad.rest.client.api.properties import ArrayProperty, BooleanProperty, ByteProperty, IntegerProperty, PathProperty, Property, SizeProperty

LOG = logging.getLogger(__name__)


class VlanResource(Resource):
    TYPE = 'vlan'
    PROPERTIES = [
        IntegerProperty('tmp-id'),
        IntegerProperty('vlan-id'),
        ArrayProperty('allowed-vlan-ids')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(VlanResource.TYPE, *args, **kwargs)


class MacResource(Resource):
    TYPE = 'mac'
    PROPERTIES = [
        IntegerProperty('tmp-id')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(MacResource.TYPE, *args, **kwargs)


class AnetResource(Resource):
    TYPE = 'anet'
    PROPERTIES = [
        IntegerProperty('id'),
        IntegerProperty('tmp-id'),
        IntegerProperty('vlan-id'),
        Property('lower-link'),
        Property('allowed-address'),
        BooleanProperty('configure-allowed-address'),
        Property('defrouter'),
        Property('allowed-dhcp-cids'),
        ArrayProperty('link-protection'),
        BooleanProperty('iov', trueValue='on', falseValue='off'),
        Property('lro'),
        Property('ring-group'),
        Property('mac-address'),
        Property('auto-mac-address')
    ]
    RESOURCE_TYPES = [
        VlanResource(),
        MacResource()
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(AnetResource.TYPE, *args, **kwargs)


class DeviceResource(Resource):
    TYPE = 'device'
    PROPERTIES = [
        IntegerProperty('id'),
        IntegerProperty('tmp-id'),
        SizeProperty('create-size'),
        Property('storage'),
        BooleanProperty('allow-partition'),
        BooleanProperty('allow-raw-io'),
        IntegerProperty('bootpri')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(DeviceResource.TYPE, *args, **kwargs)


class CappedMemoryResource(Resource):
    TYPE = 'capped-memory'
    PROPERTIES = [
        ByteProperty('physical'),
        Property('pagesize-policy')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(CappedMemoryResource.TYPE, *args, **kwargs)


class NcpusProperty(Property):
    def decode(self, value):
        try:
            return int(value)
        except ValueError:
            return value


class VirtualCpuResource(Resource):
    TYPE = 'virtual-cpu'
    PROPERTIES = [
        NcpusProperty('ncpus')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(VirtualCpuResource.TYPE, *args, **kwargs)


class CappedCpuResource(Resource):
    TYPE = 'capped-cpu'
    PROPERTIES = [
        NcpusProperty('ncpus')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(CappedCpuResource.TYPE, *args, **kwargs)


class DedicatedCpuResource(Resource):
    TYPE = 'dedicated-cpu'
    PROPERTIES = [
        NcpusProperty('ncpus')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(DedicatedCpuResource.TYPE, *args, **kwargs)



class SuspendResource(Resource):
    TYPE = 'suspend'
    PROPERTIES = [
        PathProperty('path')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(SuspendResource.TYPE, *args, **kwargs)


class KeysourceResource(Resource):
    TYPE = 'keysource'
    PROPERTIES = [
        Property('raw')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(KeysourceResource.TYPE, *args, **kwargs)


class GlobalResource(Resource):
    TYPE = 'global'
    PROPERTIES = [
        Property('zonename'),
        PathProperty('zonepath'),
        Property('brand'),
        BooleanProperty('autoboot'),
        Property('autoshutdown'),
        Property('bootargs'),
        Property('file-mac-profile'),
        Property('pool'),
        Property('scheduling-class'),
        Property('ip-type'),
        Property('hostid'),
        Property('tenant'),
        Property('cpu-arch'),
        Property('boot-priority'),
        Property('host-compatible'),
        Property('boot-disk-protection')
    ]
    RESOURCE_TYPES = [
        AnetResource(),
        DeviceResource(),
        CappedMemoryResource(),
        VirtualCpuResource(),
        CappedCpuResource(),
        DedicatedCpuResource(),
        SuspendResource(),
        KeysourceResource()
    ]

    def __new__(cls, type=None, filter=None):
        if type is not None:
            concrete_class = ZoneResourceFactory.get_type(type)
            return concrete_class()
        return super(GlobalResource, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(GlobalResource.TYPE, *args, **kwargs)


class ZoneResourceFactory:
    @staticmethod
    def get_type(resource_type):
        resources = [GlobalResource, AnetResource, DeviceResource, VlanResource, MacResource,
                     CappedMemoryResource, VirtualCpuResource, CappedCpuResource, DedicatedCpuResource, SuspendResource, KeysourceResource]
        for resource in resources:
            if resource.TYPE == resource_type:
                return resource
        raise RADException('No such a resource with type %s' % resource_type)

    @staticmethod
    def from_json(json):
        resource_type = json.get('type')
        if resource_type is None:
            raise RADException('Argument does not have a type %s' % json)
        type = ZoneResourceFactory.get_type(resource_type)
        resource = type()
        resource.load(json)
        return resource
