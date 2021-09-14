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

from rad.rest.client import RADError, RADException
from rad.rest.client.api.rad_interface import RADInterface
from rad.rest.client.api.rad_response import RADResponse
from rad.rest.client.api.authentication import RAD_NAMESPACE, RAD_API_VERSION

LOG = logging.getLogger(__name__)


class RADSession(RADInterface):
    RAD_COLLECTION = 'Session'

    def __init__(self, hostname, port=6788, ssl_cert_verify=False, ssl_cert_path=None):
        super().__init__(RAD_NAMESPACE, RADSession.RAD_COLLECTION, RAD_API_VERSION)
        self.hostname = hostname
        self.port = port
        self.verify = ssl_cert_verify
        if ssl_cert_path is not None:
            self.verify = ssl_cert_path

        self.session = None
        self.session_file = '/tmp/{}_{}.dat'.format(hostname, port)
        self.max_session_time = 30 * 60

    def __enter__(self):
        self.load_session()
        #self.login()
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
                    self.verify = pickle.load(f)
                    self.rad_instance_id = pickle.load(f)
                    was_read_from_cache = True
                    LOG.debug("Loaded session from cache (last access %ds ago) "
                              % last_modification)
        if not was_read_from_cache:
            self.session = requests.Session()
            self.session.verify = self.verify
            LOG.debug('Created new session')
            self.save_session()

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def save_session(self):
        with open(self.session_file, "wb") as f:
            pickle.dump(self.session, f)
            pickle.dump(self.verify, f)
            pickle.dump(self.rad_instance_id, f)
            LOG.debug("Saved session to cache")

    def request(self, method, path=None, **kwargs):
        if path is None:
            url = '{}/{}'.format(self.url, self.href)
        else:
            url = '{}/{}{}'.format(self.url, self.href, path)
        res = self.session.request(method, url, **kwargs)
        return RADResponse(res)

    def login(self, username, password):
        config_json = {
            "username": username,
            "password": password,
            "scheme": "pam",
            "preserve": True,
            "timeout": -1
        }
        response = self.request("POST", json=config_json)
        if response.status != 'success':
            LOG.debug('Login to %s as %s failed' %
                      (self.hostname, self.username))
            raise RADError(message='Login Failed')
        self.href = response.payload.get('href')
        self.save_session()
        LOG.debug('Login to %s as %s succeded with namespace with href %s' %
                  (self.hostname, username, self.href))

    def list_objects(self, rad_object):
        if rad_object.rad_instance_id is not None:
            raise RADException('Can not list instances from an instance')
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
        if rad_object.rad_instance_id is None:
            raise RADException('Can not get instance from a collection')
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
