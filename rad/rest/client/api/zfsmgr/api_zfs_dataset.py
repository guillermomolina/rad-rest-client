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

from rad.rest.client.api.zfsmgr import RAD_NAMESPACE
from rad.rest.client.api.api_interface import ApiInterface


class ApiZfsDataset(ApiInterface):
    RAD_COLLECTION = 'ZfsDataset'

    def __init__(self, payload=None, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, ApiZfsDataset.RAD_COLLECTION,
                         rad_api_version='1.0', *args, **kwargs)
        if payload is not None:
            self.load(payload)

    def load(self, payload):
        self.json = payload

    def get_filesystems(self, recursive=False):
        json_body = {"recursive": recursive}

        return self.rad_method('get_filesystems', json_body)