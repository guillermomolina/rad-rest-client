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

from rad.rest.client.api.rad_interface import RADInterface
from rad.rest.client.api.kstat_2 import RAD_API_VERSION, RAD_NAMESPACE

class Nv():
    def __init__(self, json=None):
        self.load(json)

    def load(self, json):
        if json is None:
            self.name = None
            self.type = None
            self.flags = None
            self.string = None
            self.strings = None
            self.integer = None
            self.integers = None
            self.kstat = None
        else:
            self.name = json.get('name')
            self.type = json.get('type')
            self.flags = json.get('flags')
            self.string = json.get('string')
            self.strings = json.get('strings')
            self.integer = json.get('integer')
            self.integers = json.get('integers')
            self.kstat = json.get('kstat')
 
class Kstat(RADInterface):
    RAD_COLLECTION = 'Kstat'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, Kstat.RAD_COLLECTION, RAD_API_VERSION,*args, **kwargs)

    def getMap(self):
        payload = self.rad_method('getMap', {})
        map = {}
        for key, value in payload.items():
            map[key] = Nv(value)
        return map


    def getFlags(self):
        return self.rad_method('getFlags', {})

    def getMapMetadata(self):
        return self.rad_method('getMapMetadata', {})

    def getNvMetadata(self):
        return self.rad_method('getNvMetadata', {})
