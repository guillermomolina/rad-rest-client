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

from rad.rest.client import RADException
from rad.rest.client.api.rad_values import RADString


class Property:
    def __init__(self, name, value=RADString()):
        self.name = name
        self.value = value
        self.json = None

    def load(self, json):
        self.json = json
        value = json.get('listvalue') or json.get('value')
        if self.name != self.json.get('name'):
            raise RADException('Could not load property %s=%s' % (
                self.json.get('name'), value))

        self.value.load(value)
