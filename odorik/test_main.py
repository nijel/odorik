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
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

import odorik
from odorik.main import main


class TestCommands(TestCase):
    """Test command line interface"""
    def test_version(self):
        """Test version printing"""
        output = StringIO()
        main(
            args=['version'],
            stdout=output
        )

        self.assertTrue(odorik.__version__ in output.getvalue())
