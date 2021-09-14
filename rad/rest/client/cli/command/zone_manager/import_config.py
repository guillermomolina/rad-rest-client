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
from rad.rest.client.api.authentication import RADSession
from rad.rest.client.api.zonemgr import RADZoneManager

LOG = logging.getLogger(__name__)


class CommandZoneManagerImportConfig:
    name = 'import-config'
    aliases = []

    @staticmethod
    def init_parser(container_subparsers, parent_parser):
        parser = container_subparsers.add_parser(CommandZoneManagerImportConfig.name,
                                                 aliases=CommandZoneManagerImportConfig.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Import configuration to a zone',
                                                 help='Import configuration to a zone')
        parser.add_argument('-n', '--no-execute',
                            action='store_true',
                            help='Do not execute the import')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-c', '--config',
                            help='Configuration string (ie: create -t SYSdefault)')
        group.add_argument('-f', '--file',
                            help='Read configuration from file')
        parser.add_argument('zonename',
                            help='Zone name')

    def __init__(self, options):
        try:
            with RADSession(options.hostname, options.port) as session:
                zone_manager = session.get_object(RADZoneManager())
                configuration = options.config
                if options.file is not None:
                    with open(options.file, "r") as f:
                        configuration = f.read()
                zone_manager.import_config(options.no_execute, options.zonename, configuration)
        except (OSError, IOError) as e:
            LOG.error(str(e))
