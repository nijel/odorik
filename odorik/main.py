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
"""Command line interface for odorik."""
from __future__ import print_function
from __future__ import unicode_literals

import sys
import json
import csv
from argparse import ArgumentParser
from datetime import datetime, timedelta
import dateutil.parser

import odorik
from odorik.config import OdorikConfig, NoOptionError


COMMANDS = {}

SORT_ORDER = [
    'id',
    'public_number',
    'sms_count',
    'call_count',
    'call_length',
    'bytes_down',
    'bytes_up',
    'bytes_total',
    'data_price',
    'call_price',
    'sms_price',
    'length',
    'ringing_length',
    'price',
]


def register_command(command):
    """Decorator to register command in command line interface."""
    COMMANDS[command.name] = command
    return command


def get_parser():
    """Create argument parser."""
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
        '--config-section',
        default='odorik',
        help='Configuration section to use'
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


def sort_key(value):
    """Key getter for sorting."""
    try:
        return '{0:02d}'.format(SORT_ORDER.index(value))
    except ValueError:
        return value


def sorted_items(value):
    """Sorted items iterator."""
    for key in sorted(value.keys(), key=sort_key):
        yield key, value[key]


def key_value(value):
    """Validate key=value parameter."""
    if '=' not in value:
        raise ValueError('Please specify --param as key=value')
    return value


class Command(object):

    """Basic command object."""

    name = ''
    description = ''

    def __init__(self, args, config, stdout=None):
        """Construct Command object."""
        self.args = args
        self.config = config
        if stdout is None:
            self.stdout = sys.stdout
        else:
            self.stdout = stdout
        self.odorik = odorik.Odorik(config=config)

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        return subparser.add_parser(
            cls.name, description=cls.description
        )

    @staticmethod
    def add_list_option(parser):
        """Add argparse argument --list."""
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all records (instead of printing summary)'
        )

    @staticmethod
    def add_line_option(parser):
        """Add argparse argument --line."""
        parser.add_argument(
            '--line',
            help='Line to use for listing'
        )

    def resolve(self, kind, value):
        """Resolve line/phone number from configuration."""
        if value is None:
            return None
        if value.isdigit():
            return value
        try:
            return self.config.get(kind, value)
        except NoOptionError:
            raise CommandError(
                'Invalid value for {0}: {1}'.format(kind, value)
            )

    @staticmethod
    def summary(values, fields):
        """Calculate summary of values."""
        result = {}
        for field in fields:
            result[field] = 0
        for value in values:
            for field in fields:
                result[field] += value[field]
        return result

    def println(self, line):
        """Print single line to output."""
        print(line, file=self.stdout)

    def print_json(self, value):
        """JSON print."""
        json.dump(value, self.stdout, indent=2)

    @staticmethod
    def format_value(value):
        """Format value for rendering."""
        if isinstance(value, float):
            return '{0:.2f}'.format(value)
        elif isinstance(value, int):
            return '{0}'.format(value)
        return value

    @classmethod
    def format_csv_value(cls, value):
        """Format value for rendering in CSV."""
        value = cls.format_value(value)
        if sys.version_info < (3, 0):
            return value.encode('utf-8')
        return value

    def print_csv(self, value, header):
        """CSV print."""
        if header is not None:
            writer = csv.DictWriter(self.stdout, header)
            writer.writeheader()
            for row in value:
                writer.writerow(
                    {k: self.format_csv_value(v) for k, v in row.items()}
                )
        elif isinstance(list(value.items())[0][1], dict):
            for key, data in sorted_items(value):
                self.println(self.format_csv_value(key))
                self.print_csv(data, None)
                self.println(self.format_csv_value(''))
        else:
            writer = csv.writer(self.stdout)
            for key, data in sorted_items(value):
                writer.writerow((key, self.format_csv_value(data)))

    def print_html(self, value, header):
        """HTML print."""
        if header is not None:
            self.println('<table>')
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
                    self.println('      <td>{0}</td>'.format(
                        self.format_value(item[key])
                    ))
                self.println('    </tr>')
            self.println('  </tbody>')
            self.println('</table>')
        elif isinstance(list(value.items())[0][1], dict):
            for key, data in sorted_items(value):
                self.println('<h1>{0}</h1>'.format(key))
                self.print_html(data, None)
        else:
            self.println('<table>')
            for key, data in sorted_items(value):
                self.println('  <tr>')
                self.println('    <th>{0}</th><td>{1}</td>'.format(
                    key, self.format_value(data)
                ))
                self.println('  </tr>')
            self.println('</table>')

    def print_text(self, value, header):
        """Text print."""
        if header is not None:
            for item in value:
                for key in header:
                    self.println('{0}: {1}'.format(
                        key, self.format_value(item[key])
                    ))
                self.println('')
        elif isinstance(list(value.items())[0][1], dict):
            for key, data in sorted_items(value):
                self.println(key)
                self.print_text(data, None)
                self.println('')
        else:
            for key, data in sorted_items(value):
                self.println('{0}: {1}'.format(
                    key, self.format_value(data)
                ))

    def print(self, value):
        """Print value."""
        header = None
        if isinstance(value, list):
            header = sorted(value[0].keys(), key=sort_key)

        if self.args.format == 'json':
            self.print_json(value)
        elif self.args.format == 'csv':
            self.print_csv(value, header)
        elif self.args.format == 'html':
            self.print_html(value, header)
        else:
            self.print_text(value, header)

    def run(self):
        """Main execution of the command."""
        raise NotImplementedError


class IntervalCommand(Command):

    """Helper class to handle date intervals."""

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(IntervalCommand, cls).add_parser(subparser)
        parser.add_argument(
            '--this-month',
            action='store_true',
            help='Show data for this month [default]'
        )
        parser.add_argument(
            '--last-month',
            action='store_true',
            help='Show data for last month'
        )
        parser.add_argument(
            '--start-date',
            type=dateutil.parser.parse,
            help='Starting datetime'
        )
        parser.add_argument(
            '--end-date',
            type=dateutil.parser.parse,
            help='Ending datetime'
        )
        return parser

    def get_interval(self):
        """Return interval based on passed flags."""
        now = datetime.now()

        if self.args.start_date and self.args.end_date:
            if self.args.start_date >= self.args.end_date:
                raise CommandError(
                    'Starting date has to be earlier than ending!'
                )
            return (self.args.start_date, self.args.end_date)
        elif self.args.start_date:
            return (self.args.start_date, now)
        elif self.args.end_date:
            raise CommandError('Can not set ending date without start!')

        if self.args.last_month:
            # Get last day of previous month
            now = now.replace(day=1) - timedelta(days=1)
            # Set to midnight
            now = now.replace(hour=23, minute=59, second=59)

        # Fallback to this month
        return (datetime(now.year, now.month, 1), now)

    def run(self):
        """Main execution of the command."""
        raise NotImplementedError


@register_command
class Version(Command):

    """Print version."""

    name = 'version'
    description = "Prints program version"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(Version, cls).add_parser(subparser)
        parser.add_argument(
            '--bare',
            action='store_true',
            help='Print only version'
        )
        return parser

    def run(self):
        """Main execution of the command."""
        if self.args.bare:
            self.println(odorik.__version__)
        else:
            self.print({'version': odorik.__version__})


@register_command
class API(Command):

    """Perform API GET."""

    name = 'api'
    description = "Performs API request"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(API, cls).add_parser(subparser)
        parser.add_argument(
            'path',
            help='API request path'
        )
        parser.add_argument(
            '--param',
            action='append',
            metavar='KEY=VALUE',
            type=key_value,
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
        """Main execution of the command."""
        params = {}
        for param in self.args.param:
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

    """Print balance."""

    name = 'balance'
    description = "Prints current balance"

    def run(self):
        """Main execution of the command."""
        self.print({'balance': self.odorik.balance()})


@register_command
class Lines(Command):

    """Print lines."""

    name = 'lines'
    description = "Prints lines information"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(Lines, cls).add_parser(subparser)
        parser.add_argument(
            '--generate-config',
            action='store_true',
            help='generate configuration file for line aliases'
        )
        return parser

    def run(self):
        """Main execution of the command."""
        lines = self.odorik.lines()
        if self.args.generate_config:
            lines = [line for line in lines if line['name']]
            self.println('[lines]')
            for line in lines:
                self.println('{0} = {1}'.format(
                    line['name'],
                    line['id']
                ))
            self.println('')
            self.println('[numbers]')
            for line in lines:
                self.println('{0} = {1}'.format(
                    line['name'],
                    line['public_number']
                ))

        else:
            self.print(lines)


@register_command
class Calls(IntervalCommand):

    """Print calls."""

    name = 'calls'
    description = "Prints calls"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(Calls, cls).add_parser(subparser)
        cls.add_list_option(parser)
        cls.add_line_option(parser)
        return parser

    def run(self):
        """Main execution of the command."""
        from_date, to_date = self.get_interval()
        calls = self.odorik.calls(
            from_date,
            to_date,
            self.resolve('lines', self.args.line),
        )
        if self.args.list:
            self.print(calls)
        else:
            self.print(
                self.summary(
                    calls,
                    ('price', 'length', 'ringing_length')
                )
            )


@register_command
class SMS(IntervalCommand):

    """Print SMS."""

    name = 'sms'
    description = "Prints SMS messages"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(SMS, cls).add_parser(subparser)
        cls.add_list_option(parser)
        cls.add_line_option(parser)
        return parser

    def run(self):
        """Main execution of the command."""
        from_date, to_date = self.get_interval()
        sms = self.odorik.sms(
            from_date,
            to_date,
            self.resolve('lines', self.args.line)
        )
        if self.args.list:
            self.print(sms)
        else:
            self.print(
                self.summary(
                    sms,
                    ('price',)
                )
            )


@register_command
class MobileData(IntervalCommand):

    """Print data usage."""

    name = 'mobile-data'
    description = "Prints mobile data usage"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(MobileData, cls).add_parser(subparser)
        cls.add_list_option(parser)
        parser.add_argument(
            '--phone',
            help='Limit listing to phone number',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='List limits for all phone numbers on account'
        )
        return parser

    def one_number(self, phone):
        """Processe data summary for one phone number."""
        from_date, to_date = self.get_interval()
        data_usage = self.odorik.mobile_data(
            from_date,
            to_date,
            phone
        )
        if self.args.list:
            return data_usage
        else:
            return self.summary(
                data_usage,
                ('bytes_total', 'bytes_down', 'bytes_up', 'price')
            )

    def run(self):
        """Main execution of the command."""
        if self.args.all:
            result = []
            for line in self.odorik.lines():
                result.append(self.one_number(line['public_number']))
                result[-1]['public_number'] = line['public_number']
            self.print(result)
        else:
            self.print(
                self.one_number(self.resolve('numbers', self.args.phone))
            )


@register_command
class SendSMS(Command):

    """Send SMS."""

    name = 'send-sms'
    description = "Sends a SMS message"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(SendSMS, cls).add_parser(subparser)
        parser.add_argument(
            'recipient',
            help='Recipient number',
        )
        parser.add_argument(
            'message',
            help='Message text'
        )
        parser.add_argument(
            '--sender',
            default='5517',
            help='Sender number',
        )
        return parser

    def run(self):
        """Main execution of the command."""
        self.odorik.send_sms(
            self.resolve('numbers', self.args.recipient),
            self.args.message,
            self.resolve('numbers', self.args.sender),
        )


@register_command
class Summary(IntervalCommand):

    """Print data usage."""

    name = 'summary'
    description = "Displays summary information for all lines"

    def process_line(self, line, from_date, to_date):
        """Processe summary for one line."""
        messages = self.odorik.sms(from_date, to_date, line['id'])
        calls = self.odorik.calls(from_date, to_date, line['id'])
        data_usage = self.odorik.mobile_data(
            from_date,
            to_date,
            line['public_number']
        )
        messages_summary = self.summary(messages, ('price',))
        calls_summary = self.summary(
            calls,
            ('price', 'length'),
        )
        data_summary = self.summary(
            data_usage,
            ('bytes_total', 'bytes_down', 'bytes_up', 'price')
        )
        return {
            'public_number': line['public_number'],
            'id': line['id'],
            'call_count': len(calls),
            'call_length': calls_summary['length'],
            'sms_count': len(messages),
            'bytes_total': data_summary['bytes_total'],
            'data_price': data_summary['price'],
            'call_price': calls_summary['price'],
            'sms_price': messages_summary['price'],
            'price': (
                data_summary['price'] +
                calls_summary['price'] +
                messages_summary['price']
            ),
        }

    def run(self):
        """Main execution of the command."""
        lines = self.odorik.lines()
        from_date, to_date = self.get_interval()
        result = {}
        for line in lines:
            result[line['name']] = self.process_line(
                line, from_date, to_date
            )
        self.print(result)


@register_command
class Callback(Command):

    """Initiate callback."""

    name = 'callback'
    description = "Initiates callback"

    @classmethod
    def add_parser(cls, subparser):
        """Create parser for command line."""
        parser = super(Callback, cls).add_parser(subparser)
        parser.add_argument(
            'caller',
            help='Caller number',
        )
        parser.add_argument(
            'recipient',
            help='Recipient number',
        )
        cls.add_line_option(parser)
        return parser

    def run(self):
        """Main execution of the command."""
        self.odorik.callback(
            self.resolve('numbers', self.args.caller),
            self.resolve('numbers', self.args.recipient),
            self.resolve('lines', self.args.line),
        )


def main(settings=None, stdout=None, args=None):
    """Execution entry point."""
    parser = get_parser()
    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    config = OdorikConfig(args.config_section)
    if settings is None:
        config.load(args.config)
    else:
        for section, key, value in settings:
            config.set(section, key, value)

    for override in ('user', 'password', 'url'):
        value = getattr(args, override)
        if value is not None:
            config.set(args.config_section, override, value)

    command = COMMANDS[args.cmd](args, config, stdout)
    try:
        command.run()
    except (CommandError, odorik.OdorikException) as error:
        print('Error: {0}'.format(error), file=sys.stderr)
        sys.exit(1)
