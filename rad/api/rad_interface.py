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

import datetime
import os
import pickle
import requests
import logging

from rad.exceptions import RADException

LOG = logging.getLogger(__name__)


class RADInterface(object):
    def __init__(self, hostname, rad_namespace, rad_collection, port=6788, rad_api_version=None, href=None):
        self.hostname = hostname
        self.port = port
        self.rad_namespace = rad_namespace
        self.rad_collection = rad_collection
        self.rad_api_version = rad_api_version
        self.rad_instance_id = None
        if href is not None:
            self.href = href

        self.session = None
        self.session_file = '/tmp/session.dat'
        self.max_session_time = 30 * 60


    @property
    def url(self):
        url = 'https://%(hostname)s:%(port)s' % {
            'hostname': self.hostname,
            'port': self.port,
        }
        return url

    @property
    def href(self):
        href = 'api/%(namespace)s/%(version)s/%(collection)s' % {
            'namespace': self.rad_namespace,
            'version': self.rad_api_version,
            'collection': self.rad_collection
        }
        if self.rad_instance_id is None:
            return href
        return '%(href)s/%(id)s' % {
            'href': href,
            'id': self.rad_instance_id
        }

    @href.setter
    def href(self, href):
        if href[0] == '/':
            href = href[1:]
        parts = href.split('/')
        if parts[0] != 'api':
            raise RADException('Malformed href uri %s' % href)
        self.rad_namespace = parts[1]
        self.rad_api_version = parts[2]
        self.rad_collection = parts[3]
        if len(parts) > 4 and parts[4] != '':
            self.rad_instance_id = '/'.join(parts[4:])
        else:
            self.rad_instance_id = None

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
            LOG.debug('Created new session with login')
            self.save_session()

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def save_session(self):
        with open(self.session_file, "wb") as f:
            pickle.dump(self.session, f)
            LOG.debug("Saved session to cache")

    def request(self, method, path, **kwargs):
        if self.session is None:
            self.load_session()

        url = '{}/{}'.format(self.url, path)
        res = self.session.request(method, url, **kwargs)

        self.save_session()
        return res
