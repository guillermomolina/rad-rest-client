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

from rad.rest.client.rad_types import RADByte, RADInteger, RADPath, RADProperty
from rad.rest.client.exceptions import RADError, RADException
from rad.rest.client.api.zfsmgr import RAD_NAMESPACE
from rad.rest.client.api.rad_interface import RADInterface


class ZfsDataset(RADInterface):
    RAD_COLLECTION = 'ZfsDataset'
    PROPERTIES = {
        'name': RADProperty('name', RADPath),
        'used': RADProperty('used', RADByte),
        'available': RADProperty('available', RADByte),
        'referenced': RADProperty('referenced', RADByte),
        'mountpoint': RADProperty('mountpoint', RADPath),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(RAD_NAMESPACE, ZfsDataset.RAD_COLLECTION, *args, **kwargs)

    def get_filesystems(self, recursive=False):
        json_body = {"recursive": recursive}

        return self.rad_method('get_filesystems', json_body)

    def get_props2(self):
        json_body = {"props": [
            # zfs help -l properties
            {"name": "name"},
            {"name": "available", "integer_val": True},
            {"name": "compressratio"},
            {"name": "creation", "integer_val": True},
            {"name": "defer_destroy"},
            {"name": "keychangedate"},
            {"name": "keystatus"},
            {"name": "mounted"},
            {"name": "origin"},
            {"name": "referenced", "integer_val": True},
            {"name": "rekeydate"},
            {"name": "type"},
            {"name": "used", "integer_val": True},
            {"name": "usedbydata", "integer_val": True},
            {"name": "usedbychildren", "integer_val": True},
            {"name": "usedbydataset", "integer_val": True},
            {"name": "usedbyrefreservation", "integer_val": True},
            {"name": "usedbysnapshots", "integer_val": True},
            {"name": "userrefs", "integer_val": True},
            {"name": "volblocksize"},
            {"name": "aclmode"},
            {"name": "refreservation"},
            {"name": "aclinherit"},
            {"name": "atime"},
            {"name": "canmount"},
            {"name": "checksum"},
            {"name": "compression"},
            {"name": "copies"},
            {"name": "dedup"},
            {"name": "devices"},
            {"name": "exec"},
            {"name": "logbias"},
            {"name": "mlslabel"},
            {"name": "mountpoint"},
            {"name": "nbmand"},
            {"name": "primarycache"},
            {"name": "quota", "integer_val": True},
            {"name": "sync"},
            {"name": "defaultuserquota", "integer_val": True},
            {"name": "defaultgroupquota", "integer_val": True},
            {"name": "readonly"},
            {"name": "recordsize"},
            {"name": "refquota", "integer_val": True},
            {"name": "refreservation", "integer_val": True},
            {"name": "reservation", "integer_val": True},
            {"name": "rstchown"},
            {"name": "secondarycache"},
            {"name": "setuid"},
            {"name": "shadow"},
            {"name": "sharenfs"},
            {"name": "sharesmb"},
            {"name": "snapdir"},
            {"name": "version"},
            {"name": "volsize", "integer_val": True},
            {"name": "vscan"},
            {"name": "xattr"},
            {"name": "zoned"},
            {"name": "casesensitivity"},
            {"name": "normalization"},
            {"name": "utf8only"},
            {"name": "encryption"},
            {"name": "multilevel"},
            {"name": "keysource"}
        ]}

        return self.rad_method('get_props', json_body)

    def get_props(self, property_names=['name', 'used', 'available',
                                        'referenced', 'mountpoint']):
        props = [property.get_definition()
                 for property in ZfsDataset.PROPERTIES.values() if property.name in property_names]
        json_body = {"props": props}
        return self.rad_method('get_props', json_body)

    def get_properties(self, property_names=None):
        rad_response = self.get_props(property_names)
        if rad_response.status != 'success':
            return
        property_instances = rad_response.payload
        properties = {}
        for property_instance in property_instances:
            if property_instance['error'] is not None:
                raise RADException(
                    property_instance['error'].get('libzfs_errstr'))
            rad_type = ZfsDataset.PROPERTIES[property_instance['name']].rad_type
            properties[property_instance['name']] = rad_type(
                property_instance['value'])
        return properties
