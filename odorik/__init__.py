# -*- coding: utf-8 -*-
#
# Copyright © 2015 Michal Čihař <michal@cihar.com>
#
# This file is part of Odorik <https://github.com/nijel/odorik>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Odorik API library."""
from __future__ import unicode_literals

try:
    from urllib import urlencode, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen

import json

__version__ = '0.4'

API_URL = 'https://www.odorik.cz/api/v1/'
DEVEL_URL = 'https://github.com/nijel/odorik'
URL = 'http://www.odorik.cz/'
USER_AGENT = 'python-odorik/{0}'.format(__version__)


class OdorikException(Exception):
    """
    Generic error.
    """


class Odorik(object):
    """Odorik API object."""
    def __init__(self, user='', password='', url=API_URL, config=None):
        """Creates the object, storing user and API password."""
        if config is not None:
            self.user = config.get(config.section, 'user')
            self.password = config.get(config.section, 'password')
            self.url = config.get(config.section, 'url')
        else:
            self.user = user
            self.password = password
            self.url = url

    def _fill_args(self, args):
        """Fills in args."""
        if args is None:
            args = {}
        args['user'] = self.user
        args['password'] = self.password
        args['user_agent'] = USER_AGENT
        return args

    @staticmethod
    def _check_response(response):
        """Checks whether response is valid."""
        if response.startswith('error '):
            raise OdorikException(response)

    def post(self, path, args=None):
        """Performs GET request on the API."""
        args = self._fill_args(args)
        url = '{0}{1}'.format(self.url, path)
        request = urlopen(url, urlencode(args).encode('utf-8'))
        return request.read().decode('utf-8')

    def get(self, path, args=None):
        """Performs GET request on the API."""
        args = self._fill_args(args)
        url = '{0}{1}?{2}'.format(
            self.url,
            path,
            urlencode(args)
        )
        request = urlopen(url)
        return request.read().decode('utf-8')

    def get_json(self, path, args=None):
        """JSON parser on top of get."""
        result = json.loads(self.get(path, args))
        if isinstance(result, dict) and 'errors' in result:
            raise OdorikException(result['errors'])
        return result

    def balance(self):
        """Gets current balance."""
        response = self.get('balance')
        self._check_response(response)
        return float(response)

    def mobile_data(self, from_date, to_date, number=None):
        """Gets data usage in given period."""
        if number is None:
            url = 'sim_cards/mobile_data.json'
        else:
            url = 'sim_cards/{0}/mobile_data.json'.format(number)
        return self.get_json(
            url,
            {'from': from_date.isoformat(), 'to': to_date.isoformat()}
        )

    def send_sms(self, recipient, message, sender='5517'):
        """Sends a SMS message."""
        response = self.post(
            'sms',
            {'sender': sender, 'recipient': recipient, 'message': message}
        )
        self._check_response(response)
        return response

    def calls(self, from_date, to_date, line=None):
        """Returns list of calls."""
        args = {
            'from': from_date.isoformat(),
            'to': to_date.isoformat()
        }
        if line is not None:
            args['line'] = line
        return self.get_json('calls.json', args)

    def sms(self, from_date, to_date, line=None):
        """Returns list of sms."""
        args = {
            'from': from_date.isoformat(),
            'to': to_date.isoformat()
        }
        if line is not None:
            args['line'] = line
        return self.get_json('sms.json', args)

    def callback(self, caller, recipient, line=None):
        """Initiates callback."""
        args = {
            'caller': caller,
            'recipient': recipient,
        }
        if line is not None:
            args['line'] = line
        response = self.post('callback', args)
        self._check_response(response)
        return response

    def lines(self):
        """Lists lines for an account."""
        return self.get_json('lines.json')
