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
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser
from xdg.BaseDirectory import load_config_paths

import odorik


class OdorikConfig(RawConfigParser):
    """
    Configuration parser wrapper with defaults.
    """
    def __init__(self):
        RawConfigParser.__init__(self)
        self.set_defaults()

    def set_defaults(self):
        """Set default values"""
        self.add_section('odorik')
        self.set('odorik', 'user', '')
        self.set('odorik', 'password', '')
        self.set('odorik', 'url', odorik.API_URL)

    def load(self, path=None):
        """
        Loads configuration from XDG paths.
        """
        if path is None:
            path = load_config_paths('odorik')
        self.read(path)
