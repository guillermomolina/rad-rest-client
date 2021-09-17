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

from rad.rest.client.rad_types import RADValueDumper, RADValueJSONEncoder
from rad.rest.client.util import print_table, order_dict_with_keys, print_parsable
from rad.rest.client.api.authentication import Session
from rad.rest.client.api.zfsmgr import ZfsDataset

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
                            choices=ZfsDataset.property_names(),
                            default=['name', 'used', 'available',
                                     'referenced', 'mountpoint'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=ZfsDataset.property_names(),
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
            zfs_dataset_instances = session.list_objects(ZfsDataset())

            zfs_datasets = []
            for zfs_dataset_instance in zfs_dataset_instances:
                zfs_datasets.append(
                    zfs_dataset_instance.get_properties(options.columns))

            # sort by key
            if options.sort_by is not None and options.sort_by in options.columns:
                zfs_datasets = sorted(
                    zfs_datasets, key=lambda i: i[options.sort_by])

            # filter columns
            # zfs_datasets = [order_dict_with_keys(zfs_dataset, options.columns)
            #                 for zfs_dataset in zfs_datasets]

            if options.json:
                print(json.dumps(zfs_datasets, indent=4, cls=RADValueJSONEncoder))
            elif options.yaml:
                print(yaml.dump(zfs_datasets, Dumper=RADValueDumper))
            elif options.delimiter is not None:
                print_parsable(zfs_datasets, options.delimiter)
            elif options.table:
                print_table(zfs_datasets)
