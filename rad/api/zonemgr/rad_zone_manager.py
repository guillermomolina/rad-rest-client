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
        self.evacuationState = payload.get('evacuationState')

    def create(self, name, path=None, template=None):
        json_body = {'name': name, 'noexecute': False}

        if template is not None:
            json_body['configuration'] = [template]

        url = '{}/{}/_rad_method/importConfig'.format(
            self.rad_session.url, self.href)
        response = RADResponse(self.rad_session.session.request(
            'PUT', url, json_body))
        if response.status != 'success':
            raise RADError(message='Request Failed')
        print(response)
