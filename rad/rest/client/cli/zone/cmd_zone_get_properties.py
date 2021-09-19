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
import json
import logging
import yaml

from rad.rest.client.rad_types import RADValueDumper
from rad.rest.client.api.authentication import Session
from rad.rest.client.api.zonemgr import Zone
from rad.rest.client.api.zonemgr.resources import ZoneResourceJSONEncoder

LOG = logging.getLogger(__name__)


class CmdZoneGetProperties:
    name = 'get-properties'
    aliases = ['get-resources', 'get']

    @staticmethod
    def init_parser(subparsers, parent_parser):
        parser = subparsers.add_parser(CmdZoneGetProperties.name,
                                       aliases=CmdZoneGetProperties.aliases,
                                       parents=[parent_parser],
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       description='Get properties of a zone',
                                       help='Get properties of a zone')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-y', '--yaml',
                           action='store_true',
                           help='Show output in yaml format')
        group.add_argument('-j', '--json',
                           action='store_true',
                           default=True,
                           help='Show output in json format')
        parser.add_argument('zonename',
                            help='Name of the zone')

    def __init__(self, options):
        with Session(options.hostname, protocol=options.protocol, port=options.port) as session:
            zone_instances = session.list_objects(Zone())

            # get zone
            zones = [
                zone for zone in zone_instances if zone.name in options.zonename]
            if len(zones) != 1:
                LOG.error('No such a zone named %s' % options.zonename)
                return
            zone = zones[0]
            properties = zone.get_properties()

            if options.json:
                print(json.dumps(properties,
                      indent=4, cls=ZoneResourceJSONEncoder))
            elif options.yaml:
                print(yaml.dump(properties, Dumper=RADValueDumper))
            else:
                self.print(properties)

    def print(self, global_resource):
        for property in global_resource.properties:
            if property.value and property.name != 'zonename':
                print('%s: %s' % (property.name, property.value))
        for resource in global_resource.resources:
            ident = '\t'
            id = resource.get('id')
            id_str = '[%s]' % id if id is not None else ''
            print('%s%s:' % (resource.type, id_str))
            for property in resource.properties:
                if property.value and property.name != 'id':
                    print('%s%s: %s' % (ident, property.name, property.value))
