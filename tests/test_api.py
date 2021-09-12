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

import unittest
from pathlib import Path

from rad.api.manager import Manager
from rad.exceptions import RADError, RADException
from rad.lib.zfs import zfs_exists, zfs_get, zfs_is_filesystem

zfs = 'rpool/my/cool/zfs/directory'
directory = '/my_cool_zfs_directory'


class TestAPI(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()



if __name__ == '__main__':
    unittest.main()
