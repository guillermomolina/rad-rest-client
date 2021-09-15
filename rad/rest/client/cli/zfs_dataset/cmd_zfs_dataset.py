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

from rad.rest.client.cli.zfs_dataset.cmd_zfs_dataset_get_filesystems import CmdZfsDatasetGetFilesystems
from rad.rest.client.cli.zfs_dataset.cmd_zfs_dataset_list import CmdZfsDatasetList

class CmdZfsDataset:
    name = 'zfs-dataset'
    aliases = []

    commands = {
        CmdZfsDatasetGetFilesystems.name: CmdZfsDatasetGetFilesystems,
        CmdZfsDatasetList.name: CmdZfsDatasetList
    }

    @staticmethod
    def init_parser(oci_subparsers):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser = oci_subparsers.add_parser(CmdZfsDataset.name,
            aliases=CmdZfsDataset.aliases,
            parents=[parent_parser],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Manage ZFS datasets',
            help='Manage ZFS datasets')

        subparsers = parser.add_subparsers(
            dest='subcommand',
            metavar='COMMAND',
            required=True)

        for subcommand in CmdZfsDataset.commands.values():
            subcommand.init_parser(subparsers, parent_parser)

    def __init__(self, options):
        command = CmdZfsDataset.commands[options.subcommand]
        command(options)
