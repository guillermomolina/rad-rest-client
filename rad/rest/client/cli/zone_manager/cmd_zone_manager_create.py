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
from rad.rest.client.api.authentication import ApiSession
from rad.rest.client.api.zonemgr import ApiZoneManager

LOG = logging.getLogger(__name__)


class CmdZoneManagerCreate:
    name = 'create'
    aliases = []

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CmdZoneManagerCreate.name,
                                                 aliases=CmdZoneManagerCreate.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Create a zone',
                                                 help='Create a zone using a template')
        parser.add_argument('-t', '--template',
                            choices=['SYSDefault'],
                            #default='SYSDefault',
                            help='Specify the template name')
        parser.add_argument('-p', '--path',
                            help='Specify the zone path')
        parser.add_argument('zonename',
                            help='Specify the zone name')

    def __init__(self, options):
        with ApiSession(options.hostname, protocol=options.protocol, port=options.port) as session:
            zone_manager = session.get_object(ApiZoneManager())
            zone_manager.create(options.zonename, options.path, options.template)
