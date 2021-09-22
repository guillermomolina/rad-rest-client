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
import urllib

from rad.rest.client import RADError, RADException, NotFoundError, ObjectError
from rad.rest.client.api.rad_response import RADResponse

LOG = logging.getLogger(__name__)


class RADInterface(object):
    def __init__(self, rad_namespace, rad_collection, rad_api_version=None, href=None, _conn=None, json=None):
        self.rad_namespace = rad_namespace
        self.rad_collection = rad_collection
        self.rad_api_version = rad_api_version or '1.0'
        self._conn = _conn
        self.rad_instance_id = None
        self.rad_reference_id = None
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
        if self.rad_instance_id is not None:
            return '%(href)s/%(id)s' % {
                'href': href,
                'id': urllib.parse.quote(self.rad_instance_id, safe=',')
            }
        if self.rad_reference_id is not None:
            return '%(href)s/_rad_reference/%(id)d' % {
                'href': href,
                'id': self.rad_reference_id
            }
        return href

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
        if len(parts) == 5 and parts[4] != '':
            self.rad_instance_id = urllib.parse.unquote(parts[4])
        else:
            self.rad_instance_id = None
        if len(parts) == 6 and parts[4] == '_rad_reference':
            self.rad_reference_id = int(parts[5])
        else:
            self.rad_reference_id = None

    def init(self):
        pass

    def request(self, method, path=None, **kwargs):
        if path is None:
            url = '{}/{}'.format(self._conn.url, self.href)
        else:
            url = '{}/{}{}'.format(self._conn.url, self.href, path)
        if self._conn is None:
            raise RADError('_conn is undefined')
        res = self._conn.session.request(method, url, **kwargs)
        return RADResponse(res)

    def rad_method(self, method, json_body, **kwargs):
        response = self.request(
            'PUT', '/_rad_method/{}'.format(method), json=json_body, **kwargs)
        if response.status != 'success':
            LOG.warning('While executing method %s on %s' %
                        (method, self.href))
            LOG.warning(response.status)
            if response.payload.get('code'):
                LOG.warning(response.payload.get('code'))
            if response.payload.get('stderr'):
                LOG.warning(response.payload.get('stderr'))
            if response.status == 'object not found':
                raise NotFoundError(response.status)
            raise ObjectError(message=response.payload.get('stderr'))
        return response.payload
