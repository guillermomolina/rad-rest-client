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
from typing import OrderedDict
import yaml

from rad.rest.client.api.authentication_1 import Session
from rad.rest.client.api.kstat_2 import Kstat

LOG = logging.getLogger(__name__)


class CmdKstatGet:
    name = 'get'
    aliases = []

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdKstatGet.name,
                                                 aliases=CmdKstatGet.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Get kstat objects',
                                                 help='Get kstat objects')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-y', '--yaml',
                           action='store_true',
                           help='Show output in yaml format')
        group.add_argument('-j', '--json',
                           action='store_true',
                           help='Show output in json format')
        parser.add_argument('uri', 
                            help='Kstat URI to retrieve information, ie: kstat:/system/cpu/0/sys')

    def __init__(self, options):
        with Session(protocol=options.protocol, hostname=options.hostname, port=options.port) as session:
            kstat_obj = session.get_object(Kstat(), {'uri': options.uri})
            map = kstat_obj.getMap()

            items = [(key, nv.integer or nv.string or nv.integers or nv.strings or nv.kstat or 0) for key, nv in map.items()]            
            resource = OrderedDict(x for x in sorted(items))

            if options.json:
                print(json.dumps(resource, indent=4))
            elif options.yaml:
                print(yaml.dump(resource))
            else:
                self.print(options.uri, resource)

    def print(self, uri, resource):
        for key, value in resource.items():
            print('%s;%s:\t%s' % (uri, key, value))
