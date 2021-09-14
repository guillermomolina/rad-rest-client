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


def print_table(table, truncate=True, separation=2, identation=0):
    MAX_COLUMN_LENGTH = 50
    if len(table) == 0:
        return

    columns = []
    # initialize columns from first row's keys
    for key in table[0]:
        columns.append({
            'key': key,
            'tittle': key.upper(),
            'length': len(key)
        })

    # adjust columns lenghts to max record sizes
    for column in columns:
        for row in table:
            value = str(row[column['key']]).replace('\t', ' ')
            row[column['key']] = value
            column['length'] = max(column['length'], len(value))

    if truncate:
        for column in columns:
            column['length'] = min(column['length'], MAX_COLUMN_LENGTH)

    separation_string = ' ' * separation

    # print headers
    strings = [''] * identation if identation > 0 else []
    for column in columns:
        str_format = '{:%s}' % str(column['length'])
        strings.append(str_format.format(column['tittle']))
    print(separation_string.join(strings))

    for row in table:
        strings = [''] * identation if identation > 0 else []
        for column in columns:
            value = row[column['key']]
            if truncate and len(value) > MAX_COLUMN_LENGTH:
                value = value[:MAX_COLUMN_LENGTH-3] + '...'
            str_format = '{:%s}' % str(column['length'])
            strings.append(str_format.format(value))
        print(separation_string.join(strings))


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB'}
    while size > power:
        size /= power
        n += 1
    return '{:.2f} {:s}'.format(size, power_labels[n])


def print_info(data):
    for key, value in data.items():
        print('%s: %s' % (key, value))
