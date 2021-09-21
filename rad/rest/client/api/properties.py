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

from functools import total_ordering
from rad.rest.client.exceptions import RADError
from rad.rest.client import RADException


@total_ordering
class Property:
    RIGHT_ALIGNED = False

    def __init__(self, name):
        self.name = name
        self.value = None
        self.json = None

    def load(self, json):
        self.json = json
        value = json.get('value')
        if self.name != self.json.get('name'):
            raise RADException('Could not load property %s=%s' % (
                self.json.get('name'), value))

        self.value = self.decode(value)

    def decode(self, value):
        return value

    def __str__(self):
        return str(self.value)
    
    def get_definition(self):
        return {'name': self.name}

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value
        

class ArrayProperty(Property):
    def load(self, json):
        self.json = json
        listvalue = json.get('listvalue')
        if self.name != self.json.get('name'):
            raise RADException('Could not load property %s=%s' % (
                self.json.get('name'), listvalue))

        self.value = [self.decode(value) for value in listvalue]


class BooleanProperty(Property):
    def __init__(self, name, trueValue='true', falseValue='false', *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.trueValue = trueValue
        self.falseValue = falseValue

    def decode(self, value):
        if value == self.trueValue:
            return True
        elif value == self.falseValue:
            return False
        else:
            raise RADException('Boolean property value %s is not %s or %s' % (
                str(value), str(self.trueValue), str(self.falseValue)))

    def __str__(self):
        return self.trueValue if self.value else self.falseValue



class PathProperty(Property):

    def decode(self, value):
        if value == '-':
            return None
        return value

    def __str__(self):
        if self.value is None:
            return '-'
        return self.value


class IntegerProperty(Property):
    RIGHT_ALIGNED = True

    def decode(self, value):
        return int(value)

    def get_definition(self):
        definition = super().get_definition()
        definition['integer_val'] = True
        return definition

class FloatProperty(Property):
    RIGHT_ALIGNED = True

    def decode(self, value):
        return float(value)


class SizeProperty(IntegerProperty):
    POWER_LABELS = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E'}

    def decode(self, value):
        try:
            return int(value)
        except:
            if str[-1] in SizeProperty.POWER_LABELS.values():                
                power = SizeProperty.POWER_LABELS
            raise RADError('NYI')

    def __str__(self):
        # 2**10 = 1024
        size = self.value
        power = 2**10
        n = 0
        power_labels = SizeProperty.POWER_LABELS
        while size > power:
            size /= power
            n += 1
        return '{:.2f} {:s}'.format(size, power_labels[n])


class ByteProperty(SizeProperty):
    UNIT_LABEL = {'B'}

    def __str__(self):
        string = super().__str__()
        return string + 'B'
