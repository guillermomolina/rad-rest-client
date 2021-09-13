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

import traceback
import logging

from rad import RADError
from rad.api.rad_interface import RADInterface
from rad.api.rad_response import RADResponse
from rad.api.authentication import RAD_NAMESPACE, RAD_API_VERSION

LOG = logging.getLogger(__name__)


class RADSession(RADInterface):
    RAD_COLLECTION = 'Session'

    def __init__(self, username, password, ssl_cert_verify=False, ssl_cert_path=None):
        super().__init__(RAD_NAMESPACE, RADSession.RAD_COLLECTION, RAD_API_VERSION)
        self.username = username
        self.password = password
        self.verify = ssl_cert_verify
        if self.verify and ssl_cert_path is not None:
            self.verify = ssl_cert_path
        self.session_id = -1

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    def login(self):
        config_json = {
            "username": self.username,
            "password": self.password,
            "scheme": "pam",
            "preserve": True,
            "timeout": -1
        }
        url = '{}/{}'.format(self.url, self.href)
        response = RADResponse(self.session.request(
            "POST", url, json=config_json, verify=self.verify))
        if response.status != 'success':
            LOG.debug('Login to %s as %s failed' %
                        (self.hostname, self.username))
            raise RADError(message='Login Failed')
        self.href = response.payload.get('href')
        parts = self.rad_instance_id.split('/')
        self.session_id = int(parts[1])
        LOG.debug('Login to %s as %s succeded with namespace %d' %
                    (self.hostname, self.username, self.session_id))

    def list_objects(self, rad_object):
        url = '{}/{}?_rad_detail'.format(self.url, rad_object.href)
        response = RADResponse(self.session.request(
            'GET', url, verify=self.verify))
        if response.status != 'success':
            raise RADError(message='Request Failed')
        output = []
        for item in response.payload:
            collection_class = rad_object.__class__
            collection = collection_class.RAD_COLLECTION
            new_rad_object = collection_class(rad_session=self, href=item.get(
                'href'), payload=item.get(collection))
            output.append(new_rad_object)
        return output

    def get_object(self, rad_object):
        url = '{}/{}?_rad_detail'.format(self.url, rad_object.href)
        response = RADResponse(self.session.request(
            'GET', url, verify=self.verify))
        if response.status != 'success':
            raise RADError(message='Request Failed')
        item = response.payload
        collection_class = rad_object.__class__
        collection = collection_class.RAD_COLLECTION
        new_rad_object = collection_class(rad_session=self, href=item.get(
            'href'), payload=item.get(collection))
        return new_rad_object
