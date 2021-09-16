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
from rad.rest.client.api.zfsmgr import ZfsDataset

LOG = logging.getLogger(__name__)


class CmdZfsList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CmdZfsList.name,
                                                 aliases=CmdZfsList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List zfs datasets',
                                                 help='List zfs datasets')
        parser.add_argument('-c', '--columns',
                            nargs='+',
                            choices=['name', 'used', 'available',
                                     'referenced', 'mountpoint'],
                            default=['name', 'used', 'available',
                                     'referenced', 'mountpoint'],
                            help='Specify wich columns to show in the table')
        parser.add_argument('-s', '--sort-by',
                            choices=['name'],
                            help='Specify the sort order in the table')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zfs_dataset_instances = session.list_objects(ZfsDataset())

            zfs_datasets = []
            for zfs_dataset_instance in zfs_dataset_instances:
                zfs_dataset = {}
                property_instances = zfs_dataset_instance.get_props()
                for property in property_instances.payload:
                    property_name = property['name']
                    property_value = property['value']
                    if property_name in ['used', 'available', 'referenced']:
                        property_value = format_bytes(int(property_value))
                    zfs_dataset[property_name] = property_value
                zfs_datasets.append(zfs_dataset)

            # sort by key
            if options.sort_by is not None:
                zones = sorted(zfs_datasets, key=lambda i: i[options.sort_by])

            # filter columns
            zfs_datasets = [order_dict_with_keys(zfs_dataset, options.columns)
                            for zfs_dataset in zfs_datasets]

            print_table(zfs_datasets)
