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


from pathlib import Path
from functools import total_ordering
from json import JSONEncoder
from rad.rest.client.exceptions import RADException
from typing import OrderedDict
from yaml import SafeDumper


@total_ordering
class RADValue:
    RIGHT_ALIGNED = False

    def __init__(self):
        self.value = None

    def load(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class RADBoolean(RADValue):
    def __init__(self, trueValue='true', falseValue='false', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trueValue = trueValue
        self.falseValue = falseValue

    def load(self, value):
        if value == self.trueValue:
            self.value = True
        elif value == self.falseValue:
            self.value = False
        else:
            raise RADException('Boolean defined value %s is not %s or %s' % (
                str(value), str(self.trueValue), str(self.falseValue)))

    def __str__(self):
        return self.trueValue if self.value else self.falseValue


class RADString(RADValue):
    pass

class RADArray(RADValue):
    pass


class RADPath(RADString):

    def load(self, value):
        self.value = value
        if value == '-':
            self.value = None

    def __str__(self):
        if self.value is None:
            return '-'
        return self.value


class RadNumber(RADValue):
    RIGHT_ALIGNED = True


class RADInteger(RadNumber):
    def load(self, value):
        self.value = int(value)


class RADFloat(RadNumber):
    def load(self, value):
        self.value = float(value)


class RADSize(RADInteger):
    POWER_LABELS = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E'}

    def __str__(self):
        # 2**10 = 1024
        size = self.value
        power = 2**10
        n = 0
        power_labels = RADSize.POWER_LABELS
        while size > power:
            size /= power
            n += 1
        return '{:.2f} {:s}'.format(size, power_labels[n])


class RADByte(RADSize):
    UNIT_LABEL = {'B'}

    def __str__(self):
        string = super().__str__()
        return string + 'B'


class RADValueJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)


class RADValueDumper(SafeDumper):
    def represent_data(self, data):
        if isinstance(data, RADValue):
            return self.represent_data(str(data))
        # if isinstance(data, Path):
        #     return super().represent_data(str(data))
        if isinstance(data, OrderedDict):
            return super().represent_data(dict(data))
        return super().represent_data(data)