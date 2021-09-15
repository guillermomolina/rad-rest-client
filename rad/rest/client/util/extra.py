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


from typing import OrderedDict


def filter_dict(dict_object, callback):
    new_dict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dict_object.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            new_dict[key] = value
    return new_dict


def order_dict_with_keys(dict_object, key_list):
    new_dict = OrderedDict()
    for key in key_list:
        new_dict[key] = dict_object[key]
    return new_dict


def list_insert_sorted_by_key(list, dict_object, key):
    for index, value in enumerate(list):
        if value.get(key) > dict_object.get(key):
            list.insert(index, dict_object)
            return
    list.append(dict_object)
