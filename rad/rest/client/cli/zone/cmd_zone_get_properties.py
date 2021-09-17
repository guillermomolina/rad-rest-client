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
from rad.rest.client.util import print_table, order_dict_with_keys
from rad.rest.client.api.authentication import Session
from rad.rest.client.api.zonemgr import Zone

LOG = logging.getLogger(__name__)


class CmdZoneGetProperties:
    name = 'get-properties'
    aliases = ['get']

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZoneGetProperties.name,
                                       aliases=CmdZoneGetProperties.aliases,
                                       parents=[parent_parser],
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       description='Get properties of a zone',
                                       help='Get properties of a zone')
        parser.add_argument('-c', '--columns',
                            nargs='+',
                            choices=['id', 'name', 'brand',
                                     'state', 'auxstate', 'uuid'],
                            default=['id', 'name', 'brand', 'state'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=['id', 'name', 'brand',
                                     'state', 'auxstate', 'uuid'],
                            help='Specify the sort order in the table')
        parser.add_argument('zonename',
                            nargs='+',
                            help='Name of the zone')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zone_instances = session.list_objects(Zone())

            # get dictionaries
            zones = [zone.json for zone in zone_instances if zone.name in options.zonename]

            # sort by key
            if options.sort_by is not None:
                zones = sorted(zones, key=lambda i: i[options.sort_by])

            # filter columns
            zones = [order_dict_with_keys(zone, options.columns)
                     for zone in zones]
            print_table(zones)