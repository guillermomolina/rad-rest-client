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
from rad.rest.client.util.print import print_table
from rad.rest.client.api.authentication import ApiSession
from rad.rest.client.api.zfsmgr import ApiZfsDataset


class CmdZfsDatasetGetFilesystems:
    name = 'get-filesystems'
    aliases = []

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CmdZfsDatasetGetFilesystems.name,
                                                 aliases=CmdZfsDatasetGetFilesystems.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Get ZFS filesystems',
                                                 help='Get ZFS filesystems')
        parser.add_argument('-s', '--sort',
                            help='Sort the filesystems')

    def __init__(self, options):
        with ApiSession(options.hostname, protocol=options.protocol, port=options.port) as session:
            zfs_dataset = ApiZfsDataset()
            zfs_dataset.rad_session = session
            zfs_dataset.rad_instance_id = 'rpool'
            print(zfs_dataset.get_filesystems().payload)
