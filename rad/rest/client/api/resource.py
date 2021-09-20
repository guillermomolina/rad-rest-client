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
import copy

from rad.rest.client import RADException
from rad.rest.client.api.property import Property
from rad.rest.client.api.rad_values import RADString

LOG = logging.getLogger(__name__)


class Resource:
    PROPERTIES = []

    @classmethod
    def get_property(cls, property_name):
        for property in cls.PROPERTIES:
            if property.name == property_name:
                return copy.deepcopy(property)
        LOG.warning('No such a property %s defined in resource %s' %
                    (property_name, cls.TYPE))
        return Property(property_name, RADString())

    @classmethod
    def get_property_names(cls):
        return [ property.name for property in cls.PROPERTIES]

    def __init__(self, type):
        self.type = type
        self.json = None
        self.resources = None
        self.properties = None

    def load(self, json):
        if self.type != json.get('type'):
            raise RADException('Could not load resource %s' %
                                json.get('type'))
        self.resources = []
        self.properties = []
        self.json = json
        for property_json in json.get('properties'):
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
