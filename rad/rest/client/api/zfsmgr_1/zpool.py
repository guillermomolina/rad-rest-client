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

from rad.rest.client.api.rad_interface import RADInterface
from rad.rest.client.api.zfsmgr_1 import RAD_NAMESPACE
from rad.rest.client.api.zfsmgr_1.zpool_resource import ZpoolResource


class Zpool(RADInterface):
    RAD_COLLECTION = 'Zpool'

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, Zpool.RAD_COLLECTION, *args, **kwargs)

    def get_props(self, property_names=None):
        if property_names is None:
            property_names = ZpoolResource.get_property_names()

        props = [property.get_definition()
                 for property in ZpoolResource.PROPERTIES if property.name in property_names]
        json_body = {"props": props}
        return self.rad_method('get_props', json_body)

    def get_properties(self, property_names=None):
        property_instances = self.get_props(property_names)
        resource = ZpoolResource()
        resource.load(property_instances)
        return resource
