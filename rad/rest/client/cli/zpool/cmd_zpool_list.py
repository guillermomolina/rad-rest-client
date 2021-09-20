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
import json
from rad.rest.client.api.zfsmgr.zpool_resource import ZpoolResource
import yaml

from rad.rest.client.api.rad_values import RADValueDumper, RADValueJSONEncoder
from rad.rest.client.util import print_table, order_dict_with_keys, print_parsable
from rad.rest.client.api.authentication import Session
from rad.rest.client.api.zfsmgr import Zpool

LOG = logging.getLogger(__name__)


class CmdZpoolList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZpoolList.name,
                                       aliases=CmdZpoolList.aliases,
                                       parents=[parent_parser],
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       description='List ZFS pools',
                                       help='List ZFS pools')
        parser.add_argument('-c', '--columns',
                            nargs='+',
                            choices=ZpoolResource.get_property_names(),
                            default=['name', 'size', 'allocated', 'free',
                                     'capacity', 'dedupratio', 'health', 'altroot'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=ZpoolResource.get_property_names(),
                            default='name',
                            help='Specify the sort order in the table')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-t', '--table',
                           action='store_true',
                           default=True,
                           help='Show output in table format')
        group.add_argument('-y', '--yaml',
                           action='store_true',
                           help='Show output in yaml format')
        group.add_argument('-j', '--json',
                           action='store_true',
                           help='Show output in json format')
        group.add_argument('-d', '--delimiter',
                           help='Show output in a parsable format delimited by the string')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zpool_instances = session.list_objects(Zpool())

            zpool_resources = [instance.get_properties(
                options.columns) for instance in zpool_instances]

            zpools = []
            for zfs_resource in zpool_resources:
                resource = {}
                for property in zfs_resource.properties:
                    resource[property.name] = property.value
                zpools.append(resource)

            # sort by key
            if options.sort_by is not None:
                zpools = sorted(zpools, key=lambda i: i[options.sort_by])

            # filter columns
            # zpools = [order_dict_with_keys(zpool, options.columns)
            #                 for zpool in zpools]

            if options.json:
                print(json.dumps(zpools, indent=4, cls=RADValueJSONEncoder))
            elif options.yaml:
                print(yaml.dump(zpools, Dumper=RADValueDumper))
            elif options.delimiter is not None:
                print_parsable(zpools, options.delimiter)
            elif options.table:
                print_table(zpools)
