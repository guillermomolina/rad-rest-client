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

from rad.rest.client.api.resource import Resource
from rad.rest.client.api.zfsmgr.zfs_property import ZfsProperty
from rad.rest.client.api.rad_values import RADPath, RADByte


class ZfsResource(Resource):
    PROPERTIES = [
        ZfsProperty('name', RADPath()),
        ZfsProperty('used', RADByte()),
        ZfsProperty('available', RADByte()),
        ZfsProperty('referenced', RADByte()),
        ZfsProperty('mountpoint', RADPath())
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

    def load(self, json):
        self.resources = []
        self.properties = []
        self.json = json
        for property_json in json:
            property_name = property_json.get('name')
            property = self.__class__.get_property(property_name)
            property.load(property_json)
            self.properties.append(property)
