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
from pathlib import Path

from rad.rest.client import RADError, RADException
from rad.rest.client.api.rad_interface import RADInterface
from rad.rest.client.api.rad_response import RADResponse
from rad.rest.client.api.authentication_1 import RAD_NAMESPACE, RAD_API_VERSION

LOG = logging.getLogger(__name__)


def modification_date(filename):
    t = filename.stat().st_mtime
    return datetime.datetime.fromtimestamp(t)


class Session(RADInterface):
    RAD_COLLECTION = 'Session'

    def __init__(self, hostname, protocol='https', port=6788):
        super().__init__(RAD_NAMESPACE, Session.RAD_COLLECTION, RAD_API_VERSION)
        self.protocol = protocol
        self.hostname = hostname
        self.port = port
        self.session = None
        self.max_session_time = 0
        filename = '~/.cache/rad/{}_{}_{}.dat'.format(
            self.protocol, self.hostname, self.port)
        self.session_filename = Path(filename).expanduser()

    def __enter__(self):
        self.load_session()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            #traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    @property
    def url(self):
        url = '%(protocol)s://%(hostname)s:%(port)s' % {
            'protocol': self.protocol,
            'hostname': self.hostname,
            'port': self.port,
        }
        return url

    def load_session(self, force=False):
        was_read_from_cache = False
        LOG.debug('Loading or generating session...')
        if self.session_filename.is_file() and not force:
            time = modification_date(self.session_filename)
            last_modification = (datetime.datetime.now() - time).seconds
            if self.max_session_time == 0 or last_modification < self.max_session_time:
                with self.session_filename.open("rb") as f:
                    self.session = pickle.load(f)
                    self.rad_instance_id = pickle.load(f)
                    was_read_from_cache = True
                    LOG.debug("Loaded session from cache (last access %ds ago) "
                              % last_modification)
        if not was_read_from_cache:
            self.session = requests.Session()
            self.rad_instance_id = None
            LOG.debug('Created new session')

    def save_session(self):
        parent = self.session_filename.parent
        if not parent.is_dir():
            parent.mkdir(parents=True)
        parent.chmod(0o700)
        with self.session_filename.open("wb") as f:
            pickle.dump(self.session, f)
            pickle.dump(self.rad_instance_id, f)
            LOG.debug("Saved session to cache")
        self.session_filename.chmod(0o600)

    def request(self, method, path=None, **kwargs):
        if path is None:
            url = '{}/{}'.format(self.url, self.href)
        else:
            url = '{}/{}{}'.format(self.url, self.href, path)
        res = self.session.request(method, url, **kwargs)
        return RADResponse(res)

    def login(self, username, password, ssl_cert_verify=False, ssl_cert_path=None):
        self.load_session(force=True)

        verify = ssl_cert_verify
        if ssl_cert_path is not None:
            verify = ssl_cert_path
        self.session.verify = verify

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
                      (self.hostname, username))
            raise RADError(message='Login Failed')
        self.href = response.payload.get('href')
        self.save_session()
        LOG.debug('Login to %s as %s succeded with namespace with href %s' %
                  (self.hostname, username, self.href))

    def list_objects(self, rad_object, detailed=True):
        # if rad_object.rad_instance_id is not None:
        #    raise RADException('Can not list instances from an instance')
        rad_object.rad_session = self
        if detailed:
            path = '?_rad_detail'
        else:
            path = None
        response = rad_object.request('GET', path)
        if response.status != 'success':
            raise RADError(message='Request Failed')
        output = []
        for item in response.payload:
            collection_class = rad_object.__class__
            collection = collection_class.RAD_COLLECTION
            new_rad_object = collection_class(rad_session=self, href=item.get(
                'href'), json=item.get(collection))
            output.append(new_rad_object)
        return output

    def get_object(self, rad_object, detailed=True):
        # if rad_object.rad_instance_id is None:
        #    raise RADException('Can not get instance from a collection')
        rad_object.rad_session = self
        if detailed:
            path = '?_rad_detail'
        else:
            path = None
        response = rad_object.request('GET', path)
        if response.status != 'success':
            LOG.error(response.status)
            raise RADError(message='Request Failed')
        item = response.payload
        collection_class = rad_object.__class__
        collection = collection_class.RAD_COLLECTION
        new_rad_object = collection_class(rad_session=self, href=item.get(
            'href'), json=item.get(collection))
        return new_rad_object
