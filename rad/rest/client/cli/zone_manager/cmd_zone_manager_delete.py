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


import argparse
import logging
from rad.rest.client.api.authentication_1 import Session
from rad.rest.client.api.zonemgr_1 import ZoneManager

LOG = logging.getLogger(__name__)


class CmdZoneManagerDelete:
    name = 'delete'
    aliases = []

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZoneManagerDelete.name,
                                                 aliases=CmdZoneManagerDelete.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Delete a zone',
                                                 help='Delete a zone')
        parser.add_argument('zonename',
                            help='Specify the zone name')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zone_manager = session.get_object(ZoneManager())
            zone_manager.rad_method_delete(options.zonename)
