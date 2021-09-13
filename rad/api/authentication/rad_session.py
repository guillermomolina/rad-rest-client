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
import datetime
import os
import pickle
import requests

from rad import RADError
from rad.api.rad_interface import RADInterface
from rad.api.rad_response import RADResponse
from rad.api.authentication import RAD_NAMESPACE, RAD_API_VERSION

LOG = logging.getLogger(__name__)


class RADSession(RADInterface):
    RAD_COLLECTION = 'Session'

    def __init__(self, hostname, username, password, port=6788, ssl_cert_verify=False, ssl_cert_path=None):
        super().__init__(RAD_NAMESPACE, RADSession.RAD_COLLECTION, RAD_API_VERSION)
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.verify = ssl_cert_verify
        if self.verify and ssl_cert_path is not None:
            self.verify = ssl_cert_path

        self.session = None
        self.session_file = '/tmp/{}.dat'.format(hostname)
        self.max_session_time = 30 * 60

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    @property
    def url(self):
        url = 'https://%(hostname)s:%(port)s' % {
            'hostname': self.hostname,
            'port': self.port,
        }
        return url

    def load_session(self, force=False):
        was_read_from_cache = False
        LOG.debug('Loading or generating session...')
        if os.path.exists(self.session_file) and not force:
            time = self.modification_date(self.session_file)
            last_modification = (datetime.datetime.now() - time).seconds
            if last_modification < self.max_session_time:
                with open(self.session_file, "rb") as f:
                    self.session = pickle.load(f)
                    was_read_from_cache = True
                    LOG.debug("Loaded session from cache (last access %ds ago) "
                              % last_modification)
        if not was_read_from_cache:
            self.session = requests.Session()
            self.session.verify = self.verify
            LOG.debug('Created new session with login')
            self.save_session()

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def save_session(self):
        with open(self.session_file, "wb") as f:
            pickle.dump(self.session, f)
            LOG.debug("Saved session to cache")

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
        LOG.debug('Login to %s as %s succeded with namespace with href %d' %
                  (self.hostname, self.username, self.href))

    def list_objects(self, rad_object):
        # TODO test rad_instance_id is None ???
        rad_object.rad_session = self
        response = rad_object.request('GET', '?_rad_detail')
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
        # TODO test rad_instance_id is not None ???
        rad_object.rad_session = self
        response = rad_object.request('GET', '?_rad_detail')
        if response.status != 'success':
            raise RADError(message='Request Failed')
        item = response.payload
        collection_class = rad_object.__class__
        collection = collection_class.RAD_COLLECTION
        new_rad_object = collection_class(rad_session=self, href=item.get(
            'href'), payload=item.get(collection))
        return new_rad_object

    def request(self, method, path, **kwargs):
        url = '{}/{}'.format(self.url, self.href + path)
        res = RADResponse(self.session.request(method, url, **kwargs))
        return res
