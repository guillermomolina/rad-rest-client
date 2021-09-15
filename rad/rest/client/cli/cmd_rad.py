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

from rad.rest.client import __version__, RADException
from rad.rest.client.cli.session import CmdSession
from rad.rest.client.cli.zone import CmdZone
from rad.rest.client.cli.zone_manager import CmdZoneManager
from rad.rest.client.cli.zpool import CmdZpool
from rad.rest.client.cli.zfs_dataset import CmdZfsDataset

LOG = logging.getLogger(__name__)


def set_log_level(log_level):
    if log_level == 'none':
        logging.disable(logging.CRITICAL)
    else:
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        logging.basicConfig(level=levels[log_level])


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass


class CmdRAD:
    commands = [CmdSession, CmdZone, CmdZoneManager, CmdZfsDataset, CmdZpool]

    def __init__(self):
        parser = argparse.ArgumentParser(
            formatter_class=CustomFormatter,
            description='A Solaris RAD Client')
        parser.add_argument('-V', '--version',
                            help='Print version information and quit',
                            action='version',
                            version='%(prog)s version ' + __version__)
        parser.add_argument('-L', '--log-level',
                            help='Set the logging level ("debug"|"info"|"warn"|"error"|"fatal")',
                            choices=[
                                'debug',
                                'info',
                                'warn',
                                'error',
                                'critical',
                                'none'
                            ],
                            metavar='LOG_LEVEL',
                            default='none')
        parser.add_argument('-D', '--debug',
                            help='Enable debug mode',
                            action='store_true')
        parser.add_argument('-Q', '--quiet',
                            help='Enable quiet mode',
                            action='store_true')
        parser.add_argument('-Z', '--protocol',
                            default='https',
                            help='Protocol for RAD REST server')
        parser.add_argument('-H', '--hostname',
                            required=True,
                            help='Hostname or ip address for RAD REST server')
        parser.add_argument('-P', '--port',
                            type=int,
                            default=6788,
                            help='Port for RAD REST server')

        subparsers = parser.add_subparsers(
            dest='command',
            metavar='COMMAND',
            required=True)

        for command in CmdRAD.commands:
            command.init_parser(subparsers)

        options = parser.parse_args()

        set_log_level(options.log_level)

        if options.debug:
            import debugpy
            debugpy.listen(('0.0.0.0', 5678))
            LOG.info("Waiting for IDE to attach...")
            debugpy.wait_for_client()

        try:
            for command in self.commands:
                if options.command == command.name or options.command in command.aliases:
                    command(options)
                    break
        except RADException as e:
            LOG.error(e.message)
            print(e.message)
            exit(-1)
