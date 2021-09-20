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

from rad.rest.client.api.zfsmgr.zfs_resource import ZfsResource
from rad.rest.client.api.zfsmgr.zfs_property import ZfsProperty
from rad.rest.client.api.rad_values import RADByte, RADPath, RADString, RADBoolean


class ZpoolResource(ZfsResource):
    PROPERTIES = [
        ZfsProperty('name', RADString()),

        ZfsProperty('allocated', RADByte()),
        ZfsProperty('altroot', RADPath()),
        ZfsProperty('autoexpand', RADBoolean()),
        ZfsProperty('autoreplace', RADBoolean()),
        ZfsProperty('bootfs', RADPath()),
        ZfsProperty('cachefile', RADPath()),
        ZfsProperty('capacity', RADByte()),
        ZfsProperty('clustered', RADBoolean()),
        ZfsProperty('dedupditto', RADString()),
        ZfsProperty('dedupratio', RADString()),
        ZfsProperty('delegation', RADBoolean()),
        ZfsProperty('failmode', RADString()),
        ZfsProperty('free', RADByte()),
        ZfsProperty('guid', RADString()),
        ZfsProperty('health', RADString()),
        ZfsProperty('lastscrub', RADString()),
        ZfsProperty('listshares', RADBoolean()),
        ZfsProperty('listsnapshots', RADBoolean()),
        ZfsProperty('readonly', RADBoolean()),
        ZfsProperty('scrubinterval', RADString()),
        ZfsProperty('size', RADByte()),
        ZfsProperty('version', RADString())
    ]
