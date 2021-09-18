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

from json.encoder import JSONEncoder
from rad.rest.client.exceptions import RADException
from rad.rest.client.api.zonemgr import RAD_NAMESPACE
from rad.rest.client.api.rad_interface import RADInterface


class Property:
    def __init__(self, json=None):
        self.json = json
        self.load()

    def load(self):
        if self.json is None:
            self.name = None
            self.type = None
            self.value = None
            self.list_value = None
        else:
            self.name = self.json.get('name')
            self.type = self.json.get('type')
            self.value = self.json.get('value')
            self.list_value = self.json.get('listvalue')


class Resource:
    def __init__(self, json=None):
        self.json = json
        self.load()

    def load(self):
        self.resources = []
        if self.json is None:
            self.type = None
            self.properties = []
        else:
            self.type = self.json.get('type')
            self.properties = [Property(json=property)
                               for property in self.json.get('properties')]

    def get(self, property_name):
        properties = [
            property for property in self.properties if property.name == property_name]
        return properties[0] if len(properties) == 1 else None

    def to_json(self):
        json = {}
        for property in self.properties:
            if property.value:
                json[property.name] = property.value
        for resource in self.resources:
            if resource.get('tmp-id') is not None:
                json.setdefault(resource.type, []).append(resource.to_json())
            else:
                json[resource.type] = resource.to_json()
        return json


class ZoneResourceJSONEncoder(JSONEncoder):
    def default(self, data):
        if isinstance(data, Resource):
            return data.to_json()
        return str(data)


class Zone(RADInterface):
    RAD_COLLECTION = 'Zone'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, Zone.RAD_COLLECTION, *args, **kwargs)

    def init(self):
        if self.json is None:
            self.id = None
            self.name = None
            self.brand = None
            self.uuid = None
            self.auxstate = None
            self.state = None
        else:
            self.id = self.json.get('id')
            self.name = self.json.get('name')
            self.brand = self.json.get('brand')
            self.uuid = self.json.get('uuid')
            self.auxstate = self.json.get('auxstate')
            self.state = self.json.get('state')

    def rad_method_getResourceProperties(self, resource_names=None):
        json_body = {"filter": {"type": "device"}}
        return self.rad_method('getResourceProperties', json_body)

    def rad_method_getResources(self, resource_type=None, resource_scope_type=None):
        json_body = {}
        if resource_type is not None:
            json_body['filter'] = {"type": resource_type}
        if resource_scope_type is not None:
            json_body['scope'] = {"type": resource_scope_type}
        return self.rad_method('getResources', json_body)

    def get_properties(self):
        rad_response = self.rad_method_getResources(resource_scope_type='anet')
        subresources = {}
        if rad_response.status == 'success' and len(rad_response.payload) > 0:
            for resource_instance in rad_response.payload:
                subresources.setdefault(resource_instance['parent'], []).append(
                    Resource(resource_instance))
        rad_response = self.rad_method_getResources()
        if rad_response.status != 'success':
            return
        resource_instances = rad_response.payload
        global_resource = None
        resources = []
        for resource_instance in resource_instances:
            resource = Resource(resource_instance)
            if resource_instance['type'] == 'anet':
                key = '%s,tmp-id=%s' % (
                    resource_instance['type'], str(resource.get('tmp-id').value))
                if key in subresources:
                    resource.resources = subresources[key]
            if resource_instance['type'] == 'global':
                global_resource = resource
            else:
                resources.append(resource)
        global_resource.resources = resources
        return global_resource
