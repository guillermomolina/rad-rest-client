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

from rad.rest.client.cli.zpool.cmd_zpool_list import CmdZpoolList

class CmdZpool:
    name = 'zpool'
    aliases = []
    commands = [CmdZpoolList]

    @staticmethod
    def init_parser(subparsers):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser = subparsers.add_parser(CmdZpool.name,
            aliases=CmdZpool.aliases,
            parents=[parent_parser],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Manage ZFS pools',
            help='Manage ZFS pools')

        subparsers = parser.add_subparsers(
            dest='subcommand',
            metavar='COMMAND',
            required=True)

        for subcommand in CmdZpool.commands:
            subcommand.init_parser(subparsers, parent_parser)

    def __init__(self, options):
        for command in self.commands:
            if options.subcommand == command.name or options.subcommand in command.aliases:
                command(options)
                break
