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
import json
import csv
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
    parser.add_argument(
        '--format',
        default='text',
        choices=('text', 'csv', 'json'),
        help='Output format to use'
    )
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

    def print(self, value):
        """
        Prints value.
        """
        header = None
        if isinstance(value, list):
            header = list(value[0].keys())

        if self.args.format == 'json':
            json.dump(value, self.stdout, indent=2)

        elif self.args.format == 'csv':
            if header:
                writer = csv.DictWriter(self.stdout, header)
                writer.writeheader()
                for row in value:
                    writer.writerow(row)
            else:
                writer = csv.writer(self.stdout)
                for key, data in value.items():
                    writer.writerow((key, data))

        else:
            if header:
                for item in value:
                    self.println('{0}'.format(item))
            else:
                for key, data in value.items():
                    self.println('{0}: {1}'.format(key, data))

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
        self.print({'version': odorik.__version__})


@register_command
class API(Command):
    """
    Performs API GET.
    """
    name = 'api'
    description = "Performs API request"

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        parser = super(API, cls).add_parser(subparser)
        parser.add_argument(
            'path',
            help='API request path'
        )
        parser.add_argument(
            '--param',
            action='append',
            default=[],
            help='Parameter to append to the call'
        )
        return parser

    def run(self):
        params = {}
        for param in self.args.param:
            if not '=' in param:
                raise Exception('Please specify --param as key=value')
            key, value = param.split('=', 1)
            params[key] = value
        if self.args.path.endswith('.json'):
            result = self.odorik.get_json(self.args.path, params)
            self.print(result)
        else:
            result = self.odorik.get(self.args.path, params)
            self.println('{0}'.format(result))


@register_command
class Balance(Command):
    """
    Prints balance.
    """
    name = 'balance'
    description = "Prints current balance"

    def run(self):
        self.print({'balance': self.odorik.balance()})


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
        parser.add_argument(
            '--phone',
            help='Limit listing to phone number'
        )
        return parser

    def run(self):
        now = datetime.now()
        phone = None
        if self.args.phone:
            phone = self.args.phone
        data_usage = self.odorik.mobile_data(
            datetime(now.year, now.month, 1),
            now,
            phone
        )
        if self.args.list:
            self.print(data_usage)
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
            self.print({
                'bytes_total': bytes_total,
                'bytes_down': bytes_down,
                'bytes_up': bytes_up,
                'price':  price,
            })


@register_command
class SendSMS(Command):
    """
    Sends SMS.
    """
    name = 'send-sms'
    description = "Sends a SMS message"

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        parser = super(SendSMS, cls).add_parser(subparser)
        parser.add_argument(
            'recipient',
            help='Recipient number'
        )
        parser.add_argument(
            'message',
            help='Message text'
        )
        parser.add_argument(
            '--sender',
            default='5517',
            help='Sender number'
        )
        return parser

    def run(self):
        self.odorik.send_sms(
            self.args.recipient,
            self.args.message,
            self.args.sender,
        )


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
