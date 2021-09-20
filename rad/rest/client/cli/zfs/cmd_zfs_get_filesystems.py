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
from rad.rest.client.exceptions import RADError
from rad.rest.client.util.print import print_table
from rad.rest.client.api.authentication_1 import Session
from rad.rest.client.api.zfsmgr_1 import ZfsDataset


class CmdZfsGetFilesystems:
    name = 'get-filesystems'
    aliases = []

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZfsGetFilesystems.name,
                                                 aliases=CmdZfsGetFilesystems.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Get ZFS filesystems',
                                                 help='Get ZFS filesystems')
        parser.add_argument('-s', '--sort',
                            help='Sort the filesystems')
        parser.add_argument('poolname',
                            nargs='*',
                            help='Name of the pool')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            raise RADError('NYI')
