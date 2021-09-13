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
from rad.api.authentication import RADSession
from rad.api.zonemgr import RADZone

LOG = logging.getLogger(__name__)

class CommandZoneList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CommandZoneList.name,
                                                 aliases=CommandZoneList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List zones',
                                                 help='List zones')

    def __init__(self, options):
        with RADSession(options.hostname, options.port) as session:
            zonelist = session.list_objects(RADZone())
