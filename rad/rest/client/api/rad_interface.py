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

from rad.rest.client import RADError, RADException
from rad.rest.client.api.rad_response import RADResponse

LOG = logging.getLogger(__name__)


class RADInterface(object):
    def __init__(self, rad_namespace, rad_collection, rad_api_version=None, href=None, rad_session=None, json=None):
        self.rad_namespace = rad_namespace
        self.rad_collection = rad_collection
        self.rad_api_version = rad_api_version or '1.0'
        self.rad_session = rad_session
        self.rad_instance_id = None
        if href is not None:
            self.href = href
        self.json = json
        self.init()

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

    def init(self):
        pass

    def request(self, method, path=None, **kwargs):
        if path is None:
            url = '{}/{}'.format(self.rad_session.url, self.href)
        else:
            url = '{}/{}{}'.format(self.rad_session.url, self.href, path)
        if self.rad_session is None:
            raise RADError('rad_session is undefined')
        res = self.rad_session.session.request(method, url, **kwargs)
        return RADResponse(res)

    def rad_method(self, method, json_body, **kwargs):
        response = self.request(
            'PUT', '/_rad_method/{}'.format(method), json=json_body, **kwargs)
        if response.status != 'success':
            LOG.error(response.status)
            LOG.error(response.payload.get('code'))
            LOG.error(response.payload.get('stderr'))
            raise RADError(message=response.payload.get('stderr'))
        return response
