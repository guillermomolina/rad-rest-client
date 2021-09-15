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

from rad.rest.client.api.zonemgr import RAD_NAMESPACE
from rad.rest.client.api.api_interface import ApiInterface



class ApiZone(ApiInterface):
    RAD_COLLECTION = 'Zone'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, ApiZone.RAD_COLLECTION, rad_api_version='1.0', *args, **kwargs)
        self.id = None
        self.name = None
        self.brand = None
        self.uuid = None
        self.auxstate = None
        self.state = None

    def load(self, payload):
        self.id = payload.get('id')
        self.name = payload.get('name')
        self.brand = payload.get('brand')
        self.uuid = payload.get('uuid')
        self.auxstate = payload.get('auxstate')
        self.state = payload.get('state')
        