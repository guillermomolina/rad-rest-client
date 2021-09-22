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

from rad.rest.client.api.zfsmgr_1.zfs_resource import ZfsResource
from rad.rest.client.api.properties import BooleanProperty, ByteProperty, PathProperty, Property


class ZpoolResource(ZfsResource):
    PROPERTIES = [
        Property('name'),

        ByteProperty('allocated'),
        PathProperty('altroot'),
        BooleanProperty('autoexpand', trueValue='on', falseValue='off'),
        BooleanProperty('autoreplace', trueValue='on', falseValue='off'),
        PathProperty('bootfs'),
        PathProperty('cachefile'),
        ByteProperty('capacity'),
        BooleanProperty('clustered', trueValue='on', falseValue='off'),
        Property('dedupditto'),
        Property('dedupratio'),
        BooleanProperty('delegation', trueValue='on', falseValue='off'),
        Property('failmode'),
        ByteProperty('free'),
        Property('guid'),
        Property('health'),
        Property('lastscrub'),
        BooleanProperty('listshares', trueValue='on', falseValue='off'),
        BooleanProperty('listsnapshots', trueValue='on', falseValue='off'),
        BooleanProperty('readonly', trueValue='on', falseValue='off'),
        Property('scrubinterval'),
        ByteProperty('size'),
        Property('version')
    ]
