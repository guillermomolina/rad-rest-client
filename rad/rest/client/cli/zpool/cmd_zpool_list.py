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
from urllib.parse import unquote
from rad.rest.client.util.print import print_table
from rad.rest.client.api.authentication import Session
from rad.rest.client.api.zfsmgr import Zpool

LOG = logging.getLogger(__name__)

class CmdZpoolList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CmdZpoolList.name,
                                                 aliases=CmdZpoolList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List zpools',
                                                 help='List zpools')
        parser.add_argument('-s', '--sort',
                            action='store_true',
                            default=False,
                            help='Specify the sort order in the table')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zpool_instances = session.list_objects(Zpool())
            # get dictionaries
            zpools = [{ 'name': unquote(zpool.rad_instance_id)} for zpool in zpool_instances]

            if options.sort:
                zpools = sorted(zpools, key=lambda i: i['name'])

            print_table(zpools)
