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

from rad.rest.client.api.zonemgr_1 import RAD_NAMESPACE
from rad.rest.client.api.rad_interface import RADInterface

LOG = logging.getLogger(__name__)


class ZoneManager(RADInterface):
    RAD_COLLECTION = 'ZoneManager'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, ZoneManager.RAD_COLLECTION, *args, **kwargs)

    def init(self):
        if self.json is None:
            self.evacuationState = None
        else:
            self.evacuationState = self.json.get('evacuationState')

    def create(self, name, path=None, template=None):
        json_body = {
            'name': name,
            'path': path,
            'template': template
        }

        return self.rad_method('create', json_body)

    def importConfig(self, noexecute, name, configuration):
        json_body = {
            'noexecute': noexecute,
            'name': name,
            'configuration': [configuration]
        }

        return self.rad_method('importConfig', json_body)

    def delete(self, name):
        json_body = {'name': name}

        return self.rad_method('delete', json_body)
