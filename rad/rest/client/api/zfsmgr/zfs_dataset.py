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

from rad.rest.client.rad_types import RADByte, RADPath
from rad.rest.client.exceptions import RADException
from rad.rest.client.api.zfsmgr import RAD_NAMESPACE, Property
from rad.rest.client.api.rad_interface import RADInterface


class ZfsDataset(RADInterface):
    RAD_COLLECTION = 'ZfsDataset'
    PROPERTIES = [
        Property('name', RADPath),
        Property('used', RADByte),
        Property('available', RADByte),
        Property('referenced', RADByte),
        Property('mountpoint', RADPath)
    ]

    @classmethod
    def property_names(cls):
        return [property.name for property in cls.PROPERTIES]

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, ZfsDataset.RAD_COLLECTION, *args, **kwargs)

    def rad_method_get_filesystems(self, recursive=False):
        json_body = {"recursive": recursive}

        return self.rad_method('get_filesystems', json_body)

    def rad_method_get_props(self, property_names=None):
        if property_names is None:
            property_names = ZfsDataset.property_names()

        props = [property.get_definition()
                 for property in ZfsDataset.PROPERTIES if property.name in property_names]
        json_body = {"props": props}
        return self.rad_method('get_props', json_body)

    def get_properties(self, property_names=None):
        rad_response = self.rad_method_get_props(property_names)
        if rad_response.status != 'success':
            return
        property_instances = rad_response.payload
        properties = {}
        for property_instance in property_instances:
            if property_instance['error'] is not None:
                raise RADException(
                    property_instance['error'].get('libzfs_errstr'))
            rad_types = [
                rad_property.rad_type for rad_property in ZfsDataset.PROPERTIES if rad_property.name == property_instance['name']]
            if len(rad_types) != 1:
                raise RADException('len(rad_types) != 1')
            properties[property_instance['name']] = rad_types[0](
                property_instance['value'])
        return properties
