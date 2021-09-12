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

from rad.api.zonemgr import RADZoneManager
from rad.api.zonemgr import RADZone
from rad.api.authentication import RADSession

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    with RADSession('server', 6788, 'nova', 'secret') as session:
        zonelist = session.list_objects(RADZone())
        print([zone.name for zone in zonelist])
        zone_manager = session.get_object(RADZoneManager())
        zone_manager.importConfig(False, 'myzone', ['create -b\nset brand=solaris\nset autoboot=true\nadd anet\nset linkname=net0\nset configure-allowed-address=true\nend\n'])
        zonelist = session.list_objects(RADZone())
        print([zone.name for zone in zonelist])
        zone_manager.delete('myzone')
        zonelist = session.list_objects(RADZone())
        print([zone.name for zone in zonelist])
