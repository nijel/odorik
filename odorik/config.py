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
    from configparser import RawConfigParser, NoOptionError
except ImportError:
    from ConfigParser import RawConfigParser, NoOptionError
from xdg.BaseDirectory import load_config_paths

import odorik

__all__ = ['NoOptionError', 'OdorikConfig']


class OdorikConfig(RawConfigParser):
    """Configuration parser wrapper with defaults."""
    def __init__(self, section='odorik'):
        RawConfigParser.__init__(self)
        self.section = section
        self.set_defaults()

    def set_defaults(self):
        """Set default values."""
        self.add_section('lines')
        self.add_section('numbers')
        self.add_section(self.section)
        self.set(self.section, 'user', '')
        self.set(self.section, 'password', '')
        self.set(self.section, 'url', odorik.API_URL)

    def load(self, path=None):
        """Loads configuration from XDG paths."""
        if path is None:
            path = load_config_paths('odorik')
        self.read(path)
