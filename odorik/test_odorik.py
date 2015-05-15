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
"""Test the module."""

from unittest import TestCase
from odorik import Odorik
from decimal import Decimal
import httpretty


def register_uris():
    """Register URIs for httpretty."""
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/balance',
        body='123.45'
    )


class OdorikTest(TestCase):
    """Testing of Odorik class"""
    @httpretty.activate
    def test_balance(self):
        """Test getting balance"""
        register_uris()
        self.assertEqual(
            Odorik().balance(),
            Decimal('123.45')
        )
