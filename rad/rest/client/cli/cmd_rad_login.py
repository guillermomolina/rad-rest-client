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
import getpass
import logging
from rad.rest.client.api.authentication_1 import Session

LOG = logging.getLogger(__name__)


class Password:

    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass()
        self.value = value

    def __str__(self):
        return self.value


class CmdLogin:
    name = 'login'
    aliases = []

    @staticmethod
    def init_parser(subparsers):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser = subparsers.add_parser(CmdLogin.name,
                                                 aliases=CmdLogin.aliases,
                                                 parents=[parent_parser],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 description='Login to RAD REST server',
                                                 help='Login to RAD REST server')
        parser.add_argument('-p', '--password',
                            type=Password,
                            default=Password.DEFAULT,
                            help='Specify password')
        parser.add_argument('--ssl-cert-verify',
                            action='store_true',
                            help='Verify SSL certificate')
        parser.add_argument('--ssl-cert-path',
                            help='Path for CA SSL certificate')
        parser.add_argument('username',
                            help='Login username')

    def __init__(self, options):
        verify = options.ssl_cert_verify
        if verify is None:
            if options.ssl_cert_path is not None:
                verify = True
            else:
                verify = False
        with Session(protocol=options.protocol, hostname=options.hostname, port=options.port) as session:
            session.login(options.username, str(options.password),
                          ssl_cert_verify=verify, ssl_cert_path=options.ssl_cert_path)
