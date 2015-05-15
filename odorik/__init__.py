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
"""Odorik API library"""
from __future__ import unicode_literals

try:
    from urllib import urlencode, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen

from decimal import Decimal

__version__ = '0.1'

API_URL = 'https://www.odorik.cz/api/v1/'


class Odorik(object):
    """Odorik API object."""
    def __init__(self, user='', password='', url=API_URL):
        """Creates the object, storing user and API password."""
        self.user = user
        self.password = password
        self.url = url

    def get(self, path, **args):
        """Performs GET request on the API."""
        if 'user' not in args:
            args['user'] = self.user
        if 'password' not in args:
            args['password'] = self.password
        url = '{0}{1}?{2}'.format(
            self.url,
            path,
            urlencode(args)
        )
        request = urlopen(url)
        return request.read()

    def balance(self):
        """Gets current balance"""
        return Decimal(self.get('balance'))
