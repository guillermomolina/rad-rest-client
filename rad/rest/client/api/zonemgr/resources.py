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
from rad.rest.client.rad_types import RADBoolean, RADInteger, RADPath, RADString, RADArray, RADByte,  RADValueJSONEncoder

LOG = logging.getLogger(__name__)


class Property:
    def __init__(self, name, rad_type=RADString):
        self.name = name
        self.rad_type = rad_type
        self.json = None
        self.value = None

    def load(self, json):
        self.json = json
        if self.name != self.json.get('name'):
            raise RADException('Could not load property %s=%s' % (
                self.json.get('name'), self.json.get('value')))
        if self.rad_type == RADArray:
            self.value = RADArray(json.get('listvalue'))
        else:
            self.value = self.rad_type(json.get('value'))


class Resource:
    PROPERTIES = []

    @classmethod
    def get_property(cls, property_name):
        for property in cls.PROPERTIES:
            if property.name == property_name:
                return property
        LOG.warning('No such a property %s defined in resource %s' %
                    (property_name, cls.TYPE))
        return Property(property_name, RADString)

    def __init__(self, type, json=None):
        self.type = type,
        self.json = json
        self.load()

    def load(self):
        self.resources = []
        self.properties = []
        if self.json is not None:
            self.type = self.json.get('type')
            if self.type != self.json.get('type'):
                raise RADException('Could not load resource %s' %
                                   self.json.get('type'))
            for property_json in self.json.get('properties'):
                if property_json.get('value') or property_json.get('listvalue'):
                    property_name = property_json.get('name')
                    property = self.__class__.get_property(property_name)
                    property.load(property_json)
                    self.properties.append(property)

    def get(self, property_name):
        properties = [
            property for property in self.properties if property.name == property_name]
        return properties[0] if len(properties) == 1 else None

    def to_json(self):
        json = {}
        for property in self.properties:
            if property.value:
                json[property.name] = property.value.value
        for resource in self.resources:
            if resource.get('tmp-id') is not None:
                json.setdefault(resource.type, []).append(resource.to_json())
            else:
                json[resource.type] = resource.to_json()
        return json


class VlanResource(Resource):
    TYPE = 'vlan'
    PROPERTIES = [
        Property('tmp-id', RADInteger),
        Property('vlan-id', RADInteger),
        Property('allowed-vlan-ids', RADArray)
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(VlanResource.TYPE, *args, **kwargs)


class AnetResource(Resource):
    TYPE = 'anet'
    PROPERTIES = [
        Property('id', RADInteger),
        Property('tmp-id', RADInteger),
        Property('lower-link'),
        Property('allowed-address'),
        Property('configure-allowed-address'),
        Property('defrouter'),
        Property('allowed-dhcp-cids'),
        Property('link-protection'),
        Property('iov'),
        Property('lro'),
        Property('ring-group'),
        Property('mac-address')
    ]
    RESOURCE_TYPES = [VlanResource()]

    def __init__(self, *args, **kwargs):
        super().__init__(AnetResource.TYPE, *args, **kwargs)


class DeviceResource(Resource):
    TYPE = 'device'
    PROPERTIES = [
        Property('id', RADInteger),
        Property('tmp-id', RADInteger),
        Property('create-size'),
        Property('storage'),
        Property('allow-partition', RADBoolean),
        Property('allow-raw-io', RADBoolean),
        Property('bootpri', RADInteger)
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(DeviceResource.TYPE, *args, **kwargs)


class CappedMemoryResource(Resource):
    TYPE = 'capped-memory'
    PROPERTIES = [
        Property('physical', RADByte),
        Property('pagesize-policy')
    ]
    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(CappedMemoryResource.TYPE, *args, **kwargs)


class GlobalResource(Resource):
    TYPE = 'global'
    PROPERTIES = [
        Property('zonename'),
        Property('zonepath', RADPath),
        Property('brand'),
        Property('autoboot', RADBoolean),
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
    RESOURCE_TYPES = [AnetResource()]

    def __init__(self, *args, **kwargs):
        super().__init__(GlobalResource.TYPE, *args, **kwargs)


class ResourceFactory:
    @staticmethod
    def get_type(resource_type):
        resources = [GlobalResource, AnetResource,
                     DeviceResource, VlanResource, CappedMemoryResource]
        for resource in resources:
            if resource.TYPE == resource_type:
                return resource
        raise RADException('No such a resource with type %s' % resource_type)

    @staticmethod
    def from_json(json):
        resource_type = json.get('type')
        if resource_type is None:
            raise RADException('Argument does not have a type %s' % json)
        type = ResourceFactory.get_type(resource_type)
        return type(json)


class ZoneResourceJSONEncoder(RADValueJSONEncoder):
    def default(self, data):
        if isinstance(data, Resource):
            return data.to_json()
        return super().default(data)
