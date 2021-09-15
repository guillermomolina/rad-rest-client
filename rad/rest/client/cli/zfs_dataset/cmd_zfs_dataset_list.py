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
from rad.rest.client.api.zfsmgr import ZfsDataset

LOG = logging.getLogger(__name__)

class CmdZfsDatasetList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CmdZfsDatasetList.name,
                                                 aliases=CmdZfsDatasetList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List zfs_datasets',
                                                 help='List zfs_datasets')
        parser.add_argument('-s', '--sort',
                            action='store_true',
                            default=False,
                            help='Specify the sort order in the table')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zfs_dataset_instances = session.list_objects(ZfsDataset())
            # get dictionaries
            zfs_datasets = [{ 'name': unquote(zfs_dataset.rad_instance_id)} for zfs_dataset in zfs_dataset_instances]

            if options.sort:
                zfs_datasets = sorted(zfs_datasets, key=lambda i: i['name'])

            print_table(zfs_datasets)
