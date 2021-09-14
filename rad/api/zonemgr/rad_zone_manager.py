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

from rad import RADError
from rad.api.rad_response import RADResponse
from rad.api.zonemgr import RAD_NAMESPACE
from rad.api.rad_interface import RADInterface


class RADZoneManager(RADInterface):
    RAD_COLLECTION = 'ZoneManager'

    def __init__(self, payload=None, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, RADZoneManager.RAD_COLLECTION,
                         rad_api_version='1.0', *args, **kwargs)
        self.evacuationState = None
        if payload is not None:
            self.load(payload)

    def load(self, payload):
        self.json = payload
        self.evacuationState = payload.get('evacuationState')

    def create(self, name, path=None, template=None):
        json_body = {
            'name': name, 
            'path': path,
            'template': template
        }

        response = self.request('PUT', '/_rad_method/create', json=json_body)
        if response.status != 'success':
            raise RADError(message='Request Failed')
        print(response)

    def import_config(self, noexecute, name, configuration):
        json_body = {
            'noexecute': noexecute,
            'name': name, 
            'configuration': configuration
        }

        response = self.request('PUT', '/_rad_method/importConfig', json=json_body)
        if response.status != 'success':
            raise RADError(message=response.payload.get('stderr'))
        print(response)

    def delete(self, name):
        json_body = {'name': name}

        response = self.request('PUT', '/_rad_method/delete', json=json_body)
        if response.status != 'success':
            raise RADError(message='Request Failed')
        print(response)
