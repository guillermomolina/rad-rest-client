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

from rad.rest.client.api.zonemgr_1 import RAD_NAMESPACE
from rad.rest.client.api.rad_interface import RADInterface
from rad.rest.client.api.zonemgr_1.zone_resources import AnetResource, ZoneResourceFactory


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

    def getResourceProperties(self, filter, properties=None):
        json_body = {}
        if filter is not None:
            json_body['filter'] = {"type": filter.type}
        if properties is not None:
            json_body['properties'] = properties
        properties = self.rad_method('getResourceProperties', json_body)
        return [filter.load_property(property) for property in properties]

    def getResources(self, filter=None, scope=None):
        json_body = {}
        if filter is not None:
            json_body['filter'] = {"type": filter.type}
        if scope is not None:
            json_body['scope'] = {"type": scope.type}
        return self.rad_method('getResources', json_body)

    def get_properties(self):
        payload = self.getResources(scope=AnetResource())
        subresources = {}
        for resource_instance in payload:
            subresources.setdefault(resource_instance['parent'], []).append(
                ZoneResourceFactory.from_json(resource_instance))
        resource_instances = self.getResources()
        global_resource = None
        resources = []
        for resource_instance in resource_instances:
            resource = ZoneResourceFactory.from_json(resource_instance)
            if resource.type == 'anet':
                key = '%s,tmp-id=%s' % (
                    resource.type, str(resource.get('tmp-id').value))
                if key in subresources:
                    resource.resources = subresources[key]
            if resource.type == 'global':
                global_resource = resource
            else:
                resources.append(resource)
        global_resource.resources = resources
        return global_resource
