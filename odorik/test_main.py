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
"""Test command line interface"""

from unittest import TestCase
from io import StringIO
import httpretty

import odorik
from odorik.main import main
from odorik.test_odorik import register_uris


class TestCommands(TestCase):
    """Test command line interface"""
    def execute(self, args):
        """Execute command and return output."""
        output = StringIO()
        main(args=args, stdout=output)
        return output.getvalue()

    def test_version(self):
        """Test version printing"""
        output = self.execute(['version'])
        self.assertTrue(odorik.__version__ in output)

    @httpretty.activate
    def test_balance(self):
        """Test getting balance"""
        register_uris()
        output = self.execute(['balance'])
        self.assertTrue('123.45' in output)

    @httpretty.activate
    def test_data_summary(self):
        """Test getting data summary"""
        register_uris()
        output = self.execute(['mobile-data'])
        self.assertTrue('price: 0.1484' in output)

    @httpretty.activate
    def test_data_number(self):
        """Test getting data summary for number"""
        register_uris()
        output = self.execute(['mobile-data', '--phone', '123456789'])
        self.assertTrue('price: 0.1484' in output)

    @httpretty.activate
    def test_data_list(self):
        """Test getting data list"""
        register_uris()
        output = self.execute(['mobile-data', '--list'])
        self.assertTrue('0.1484' in output)
