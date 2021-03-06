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
from rad.rest.client.api.zfsmgr_1 import ZfsDataset
from rad.rest.client.api.zfsmgr_1.zfs_resource import ZfsResource

LOG = logging.getLogger(__name__)


class CmdZfsList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZfsList.name,
                                                 aliases=CmdZfsList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List zfs datasets',
                                                 help='List zfs datasets')
        parser.add_argument('-c', '--columns',
                            nargs='+',
                            choices=ZfsResource.get_property_names(),
                            default=['name', 'used', 'available',
                                     'referenced', 'mountpoint'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=ZfsResource.get_property_names(),
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
            zfs_dataset_instances = session.list_objects(ZfsDataset())

            zfs_resources = [instance.get_properties(options.columns) for instance in zfs_dataset_instances]

            zfs_datasets = []
            for zfs_resource in zfs_resources:
                resource = {}
                for property in zfs_resource.properties:
                    resource[property.name] = property
                zfs_datasets.append(resource)

            # sort by key
            if options.sort_by is not None and options.sort_by in options.columns:
                zfs_datasets = sorted(
                    zfs_datasets, key=lambda i: i[options.sort_by])

            if options.json:
                resources = [resource.to_json() for resource in zfs_resources]
                print(json.dumps(resources, indent=4))
            elif options.yaml:
                resources = [resource.to_json() for resource in zfs_resources]
                print(yaml.dump(resources))
            elif options.delimiter is not None:
                print_parsable(zfs_datasets, options.delimiter)
            elif options.table:
                print_table(zfs_datasets)
