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
import yaml

from rad.rest.client.util import print_table, print_parsable
from rad.rest.client.api.authentication_1 import Session
from rad.rest.client.api.zfsmgr_1 import Zpool
from rad.rest.client.api.zfsmgr_1.zpool_resource import ZpoolResource

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
        with Session(protocol=options.protocol, hostname=options.hostname, port=options.port) as session:
            zpool_instances = session.list_objects(Zpool())

            zpool_resources = [instance.get_properties(
                options.columns) for instance in zpool_instances]

            zpools = []
            for zfs_resource in zpool_resources:
                resource = {}
                for property in zfs_resource.properties:
                    resource[property.name] = property
                zpools.append(resource)

            # sort by key
            if options.sort_by is not None:
                zpools = sorted(zpools, key=lambda i: i[options.sort_by])

            if options.json:
                resources = [resource.to_json() for resource in zpool_resources]
                print(json.dumps(resources, indent=4))
            elif options.yaml:
                resources = [resource.to_json() for resource in zpool_resources]
                print(yaml.dump(resources))
            elif options.delimiter is not None:
                print_parsable(zpools, options.delimiter)
            elif options.table:
                print_table(zpools)
