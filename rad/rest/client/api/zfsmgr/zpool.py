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
from rad.rest.client.api.rad_interface import RADInterface

"""
$ zpool help -l properties
PROPERTY       EDIT  VALUES
allocated        NO  <size>
altroot         YES  <path>
autoexpand      YES  on | off
autoreplace     YES  on | off
bootfs          YES  <filesystem>
cachefile       YES  <file> | none
capacity         NO  <size>
clustered       YES  on | off
dedupditto      YES  <threshold (min 100)>
dedupratio       NO  <1.00x or higher if deduped>
delegation      YES  on | off
failmode        YES  wait | continue | panic
free             NO  <size>
guid            YES  <guid>
health           NO  <state>
lastscrub        NO  <last scrub time>
listshares      YES  on | off
listsnapshots   YES  on | off
readonly        YES  on | off
scrubinterval   YES  manual | <count> <h | d | w | m | y>
size             NO  <size>
version         YES  <version>
"""

class Zpool(RADInterface):
    RAD_COLLECTION = 'Zpool'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, Zpool.RAD_COLLECTION,
                         rad_api_version='1.0', *args, **kwargs)

    def get_props(self, recursive=False):
        json_body = {"props": [
            { "name": "name" },
            { "name": "allocated", "integer_val": True },
            { "name": "altroot" },
            { "name": "autoexpand" },
            { "name": "autoreplace" },
            { "name": "bootfs" },
            { "name": "cachefile" },
            { "name": "capacity", "integer_val": True },
            { "name": "clustered" },
            { "name": "dedupditto" },
            { "name": "dedupratio" },
            { "name": "delegation" },
            { "name": "failmode" },
            { "name": "free", "integer_val": True },
            { "name": "guid" },
            { "name": "health" },
            { "name": "lastscrub" },
            { "name": "listshares" },
            { "name": "listsnapshots" },
            { "name": "readonly" },
            { "name": "scrubinterval" },
            { "name": "size", "integer_val": True },
            { "name": "version" },
        ]}

        return self.rad_method('get_props', json_body)
