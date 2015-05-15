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
'''
Command line interface for odorik.
'''
from __future__ import print_function
from __future__ import unicode_literals

import sys
from xdg.BaseDirectory import load_config_paths
from argparse import ArgumentParser
from datetime import datetime
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

import odorik


COMMANDS = {}


def register_command(command):
    """
    Decorator to register command in command line interface.
    """
    COMMANDS[command.name] = command
    return command


class OdorikConfig(RawConfigParser):
    """
    Configuration parser wrapper with defaults.
    """
    def __init__(self):
        RawConfigParser.__init__(self)
        # Set defaults
        self.add_section('odorik')
        self.set('odorik', 'user', '')
        self.set('odorik', 'password', '')
        self.set('odorik', 'url', odorik.API_URL)

    def load(self):
        """
        Loads configuration from XDG paths.
        """
        self.read(load_config_paths('odorik'))


def get_parser():
    """
    Creates argument parser.
    """
    parser = ArgumentParser()
    subparser = parser.add_subparsers(dest="cmd")

    for command in COMMANDS:
        COMMANDS[command].add_parser(subparser)

    return parser


class Command(object):
    """
    Basic command object.
    """
    name = ''
    description = ''

    def __init__(self, args, config, stdout=None):
        self.args = args
        self.config = config
        if stdout is None:
            self.stdout = sys.stdout
        else:
            self.stdout = stdout
        self.odorik = odorik.Odorik(
            config.get('odorik', 'user'),
            config.get('odorik', 'password'),
            config.get('odorik', 'url'),
        )

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        return subparser.add_parser(
            cls.name, description=cls.description
        )

    def println(self, line):
        """
        Prints single line to output.
        """
        print(line, file=self.stdout)

    def run(self):
        """
        Main execution of the command.
        """
        raise NotImplementedError


@register_command
class Version(Command):
    """
    Prints version.
    """
    name = 'version'
    description = "Prints program version"

    def run(self):
        self.println(odorik.__version__)


@register_command
class Balance(Command):
    """
    Prints balance.
    """
    name = 'balance'
    description = "Prints current balance"

    def run(self):
        self.println('{0}'.format(self.odorik.balance()))


@register_command
class MobileData(Command):
    """
    Prints data usage.
    """
    name = 'mobile-data'
    description = "Prints mobile data usage"

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        parser = super(MobileData, cls).add_parser(subparser)
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all records (instead of printing summary)'
        )
        return parser

    def run(self):
        now = datetime.now()
        data_usage = self.odorik.mobile_data(
            datetime(now.year, now.month, 1),
            now
        )
        if self.args.list:
            for item in data_usage:
                self.println(item)
        else:
            bytes_total = 0
            bytes_down = 0
            bytes_up = 0
            price = 0
            for item in data_usage:
                bytes_total += item['bytes_total']
                bytes_down += item['bytes_down']
                bytes_up += item['bytes_up']
                price += item['price']
            self.println('bytes_total: {0}'.format(bytes_total))
            self.println('bytes_down: {0}'.format(bytes_down))
            self.println('bytes_up: {0}'.format(bytes_up))
            self.println('price: {0}'.format(price))


def main(settings=None, stdout=None, args=None):
    """
    Execution entry point.
    """
    parser = get_parser()
    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    config = OdorikConfig()
    if settings is None:
        config.load()
    else:
        for section, key, value in settings:
            config.set(section, key, value)

    command = COMMANDS[args.cmd](args, config, stdout)
    command.run()
