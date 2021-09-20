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


# TODO: use from prettytable import PrettyTable ?


from rad.rest.client.api.rad_values import RADValue


def print_table(data, truncate=True, separation=2, identation=0):
    MAX_COLUMN_LENGTH = 50
    if len(data) == 0:
        return

    columns = []
    # initialize columns from first row's keys
    for key in data[0]:
        columns.append({
            'key': key,
            'tittle': key.upper(),
            'length': len(key)
        })

    table = []
    # adjust columns lenghts to max record sizes
    for data_row in data:
        row = {}
        for column in columns:
            value = str(data_row[column['key']]).replace('\t', ' ')
            row[column['key']] = value
            column['length'] = max(column['length'], len(value))
        table.append(row)

    if truncate:
        for column in columns:
            column['length'] = min(column['length'], MAX_COLUMN_LENGTH)

    separation_string = ' ' * separation

    # print headers
    strings = [''] * identation if identation > 0 else []
    for column in columns:
        data_value = data[0][column['key']]
        if isinstance(data_value, RADValue) and data_value.__class__.RIGHT_ALIGNED:
            str_format = '{:>%s}' % str(column['length'])
        else:
            str_format = '{:%s}' % str(column['length'])
        strings.append(str_format.format(column['tittle']))
    print(separation_string.join(strings))

    for i, row in enumerate(table):
        data_row = data[i]
        strings = [''] * identation if identation > 0 else []
        for column in columns:
            value = row[column['key']]
            data_value = data_row[column['key']]
            if truncate and len(value) > MAX_COLUMN_LENGTH:
                value = value[:MAX_COLUMN_LENGTH-3] + '...'
            if isinstance(data_value, RADValue) and data_value.__class__.RIGHT_ALIGNED:
                str_format = '{:>%s}' % str(column['length'])
            else:
                str_format = '{:%s}' % str(column['length'])
            strings.append(str_format.format(value))
        print(separation_string.join(strings))

def print_parsable(data, delimiter='|'):
    if len(data) == 0:
        return

    print(delimiter.join([key.upper() for key in data[0]]))
    for item in data:
        print(delimiter.join([str(value) for value in item.values()]))
