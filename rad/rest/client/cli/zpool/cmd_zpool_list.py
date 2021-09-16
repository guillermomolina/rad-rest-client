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
from rad.rest.client.util import print_table, order_dict_with_keys, format_bytes
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
        parser.add_argument('-c', '--columns',
                            nargs='+',
                            choices=['name', 'size', 'allocated', 'free',
                                     'capacity', 'dedupratio', 'health', 'altroot'],
                            default=['name', 'size', 'allocated', 'free',
                                     'capacity', 'dedupratio', 'health', 'altroot'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=['name'],
                            help='Specify the sort order in the table')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zpool_instances = session.list_objects(Zpool())

            zpools = []
            for zpool_instance in zpool_instances:
                zpool = {}
                property_instances = zpool_instance.get_props()
                for property in property_instances.payload:
                    property_name = property['name']
                    property_value = property['value']
                    if property_name in ['size', 'allocated', 'free']:
                        property_value = format_bytes(int(property_value))
                    if property_name == 'capacity':
                        property_value = property_value + ' %'
                    zpool[property_name] = property_value
                zpools.append(zpool)

            # sort by key
            if options.sort_by is not None:
                zones = sorted(zpools, key=lambda i: i[options.sort_by])

            # filter columns
            zpools = [order_dict_with_keys(zpool, options.columns)
                      for zpool in zpools]

            print_table(zpools)
