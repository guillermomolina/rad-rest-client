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
from rad.rest.client.exceptions import RADError
from rad.rest.client.api.kstat_2.control import Control
import yaml

from rad.rest.client.util import print_table, print_parsable
from rad.rest.client.api.authentication_1 import Session
from rad.rest.client.api.kstat_2 import Kstat

LOG = logging.getLogger(__name__)


class CmdKstatList:
    name = 'list'
    aliases = ['ls']

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdKstatList.name,
                                                 aliases=CmdKstatList.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='List kstat datasets',
                                                 help='List kstat datasets')
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
            control = session.get_object(Control())
            control.update()         
            kstat_obj = session.get_object(Kstat(), {'uri': 'kstat:/zones/ops/cpu/accum/sys'})

            raise RADError('NYI')
            kstat_dataset_instances = session.list_objects(Kstat())

            kstat_resources = [instance.get_properties(options.columns) for instance in kstat_dataset_instances]

            kstat_datasets = []
            for kstat_resource in kstat_resources:
                resource = {}
                for property in kstat_resource.properties:
                    resource[property.name] = property
                kstat_datasets.append(resource)

            # sort by key
            if options.sort_by is not None and options.sort_by in options.columns:
                kstat_datasets = sorted(
                    kstat_datasets, key=lambda i: i[options.sort_by])

            if options.json:
                resources = [resource.to_json() for resource in kstat_resources]
                print(json.dumps(resources, indent=4))
            elif options.yaml:
                resources = [resource.to_json() for resource in kstat_resources]
                print(yaml.dump(resources))
            elif options.delimiter is not None:
                print_parsable(kstat_datasets, options.delimiter)
            elif options.table:
                print_table(kstat_datasets)
