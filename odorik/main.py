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
from argparse import ArgumentParser
from datetime import datetime

import odorik
from odorik.config import OdorikConfig


COMMANDS = {}


def register_command(command):
    """
    Decorator to register command in command line interface.
    """
    COMMANDS[command.name] = command
    return command


def get_parser():
    """
    Creates argument parser.
    """
    parser = ArgumentParser(
        description='Odorik <{0}> command line utility.'.format(odorik.URL),
        epilog='This utility is developed at <{0}>.'.format(odorik.DEVEL_URL),
    )
    parser.add_argument(
        '--format',
        default='text',
        choices=('text', 'csv', 'json', 'html'),
        help='Output format to use'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='odorik {0}'.format(odorik.__version__)
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file',
    )
    parser.add_argument(
        '--user',
        help='API username',
    )
    parser.add_argument(
        '--password',
        help='API password',
    )
    parser.add_argument(
        '--url',
        help='API URL',
    )
    subparser = parser.add_subparsers(dest="cmd")

    for command in COMMANDS:
        COMMANDS[command].add_parser(subparser)

    return parser


class CommandError(Exception):
    """Generic error from command line."""


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
        self.odorik = odorik.Odorik(config=config)

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

    def print_json(self, value):
        """JSON print"""
        json.dump(value, self.stdout, indent=2)

    def print_csv(self, value, header):
        """CSV print"""
        if header:
            writer = csv.DictWriter(self.stdout, header)
            writer.writeheader()
            for row in value:
                writer.writerow(row)
        else:
            writer = csv.writer(self.stdout)
            for key, data in value.items():
                writer.writerow((key, data))

    def print_html(self, value, header):
        """HTML print"""
        self.println('<table>')
        if header:
            self.println('  <thead>')
            self.println('    <tr>')
            for key in header:
                self.println('      <th>{0}</th>'.format(key))
            self.println('    </tr>')
            self.println('  </thead>')
            self.println('  <tbody>')

            for item in value:
                self.println('    <tr>')
                for key in header:
                    self.println('      <td>{0}</td>'.format(item[key]))
                self.println('    </tr>')
            self.println('  </tbody>')
        else:
            for key, data in value.items():
                self.println('  <tr>')
                self.println('    <th>{0}</th><td>{1}</td>'.format(key, data))
                self.println('  </tr>')
        self.println('</table>')

    def print_text(self, value, header):
        """Text print"""
        if header:
            for item in value:
                for key in header:
                    self.println('{0}: {1}'.format(key, item[key]))
                self.println('')
        else:
            for key, data in value.items():
                self.println('{0}: {1}'.format(key, data))

    def print(self, value):
        """
        Prints value.
        """
        header = None
        if isinstance(value, list):
            header = list(value[0].keys())

        if self.args.format == 'json':
            self.print_json(value)
        elif self.args.format == 'csv':
            self.print_csv(value, header)
        elif self.args.format == 'html':
            self.print_html(value, header)
        else:
            self.print_text(value, header)

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

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        parser = super(Version, cls).add_parser(subparser)
        parser.add_argument(
            '--bare',
            action='store_true',
            help='Print only version'
        )

    def run(self):
        if self.args.bare:
            self.println(odorik.__version__)
        else:
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
            metavar='KEY=VALUE',
            default=[],
            help='Parameter to append to the call'
        )
        parser.add_argument(
            '--post',
            action='store_true',
            help='perform POST request instead of GET'
        )
        return parser

    def run(self):
        params = {}
        for param in self.args.param:
            if '=' not in param:
                raise CommandError('Please specify --param as key=value')
            key, value = param.split('=', 1)
            params[key] = value
        if self.args.post:
            result = self.odorik.post(self.args.path, params)
            self.println('{0}'.format(result))
        elif self.args.path.endswith('.json'):
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
class Lines(Command):
    """
    Prints lines.
    """
    name = 'lines'
    description = "Prints lines information"

    def run(self):
        self.print(self.odorik.lines())


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
        parser.add_argument(
            '--all',
            action='store_true',
            help='List limits for all phone numbers on account'
        )
        return parser

    def one_number(self, phone):
        now = datetime.now()
        data_usage = self.odorik.mobile_data(
            datetime(now.year, now.month, 1),
            now,
            phone
        )
        if self.args.list:
            return data_usage
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
            return {
                'bytes_total': bytes_total,
                'bytes_down': bytes_down,
                'bytes_up': bytes_up,
                'price':  price,
            }

    def run(self):
        phone = None
        if self.args.all:
            result = []
            for line in self.odorik.lines():
                result.append(self.one_number(line['public_number']))
                result[-1]['public_number'] = line['public_number']
            self.print(result)
        else:
            if self.args.phone:
                phone = self.args.phone
            self.print(self.one_number(phone))


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


@register_command
class Callback(Command):
    """
    Initiates callback
    """
    name = 'callback'
    description = "Initiates callback"

    @classmethod
    def add_parser(cls, subparser):
        """
        Creates parser for command line.
        """
        parser = super(Callback, cls).add_parser(subparser)
        parser.add_argument(
            'caller',
            help='Caller number'
        )
        parser.add_argument(
            'recipient',
            help='Recipient number'
        )
        parser.add_argument(
            '--line',
            help='Line to use for accounting'
        )
        return parser

    def run(self):
        self.odorik.callback(
            self.args.caller,
            self.args.recipient,
            self.args.line,
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
        config.load(args.config)
    else:
        for section, key, value in settings:
            config.set(section, key, value)

    for override in ('user', 'password', 'url'):
        value = getattr(args, override)
        if value is not None:
            config.set('odorik', override, value)

    command = COMMANDS[args.cmd](args, config, stdout)
    try:
        command.run()
    except (CommandError, odorik.OdorikException) as error:
        print('Error: {0}'.format(error), file=sys.stderr)
        sys.exit(1)
