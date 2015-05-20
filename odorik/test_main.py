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
from __future__ import unicode_literals

from unittest import TestCase
from io import StringIO, BytesIO
import httpretty
import json
import sys
import os

import odorik
from odorik.main import main
from odorik.config import OdorikConfig
from odorik.test_odorik import register_uris

TEST_CONFIG = os.path.join(os.path.dirname(__file__), 'test_data', 'odorik')
TEST_SECTION = os.path.join(os.path.dirname(__file__), 'test_data', 'section')


def execute(args, binary=False, settings=None, stdout=None):
    """Execute command and return output."""
    if settings is None:
        settings = ()
    elif not settings:
        settings = None
    if binary and sys.version_info < (3, 0):
        output = BytesIO()
    else:
        output = StringIO()
    backup = sys.stdout
    try:
        sys.stdout = output
        if stdout:
            stdout = output
        main(args=args, settings=settings, stdout=stdout)
    finally:
        sys.stdout = backup
    return output.getvalue()


class TestSettings(TestCase):
    """
    Test settings handling.
    """
    @httpretty.activate
    def test_commandline(self):
        register_uris()
        output = execute(['--url', 'https://example.net/', 'balance'])
        self.assertIn('321.09', output)

    @httpretty.activate
    def test_stdout(self):
        register_uris()
        output = execute(['balance'], stdout=True)
        self.assertIn('123.45', output)

    @httpretty.activate
    def test_settings(self):
        register_uris()
        output = execute(
            ['balance'],
            settings=(('odorik', 'url', 'https://example.net/'),)
        )
        self.assertIn('321.09', output)

    @httpretty.activate
    def test_config(self):
        register_uris()
        output = execute(['--config', TEST_CONFIG, 'balance'], settings=False)
        self.assertIn('321.09', output)

    @httpretty.activate
    def test_config_section(self):
        register_uris()
        output = execute(
            [
                '--config', TEST_SECTION,
                '--config-section', 'custom',
                'balance'
            ],
            settings=False
        )
        self.assertIn('321.09', output)

    def test_parsing(self):
        config = OdorikConfig()
        self.assertEqual(config.get('odorik', 'url'), odorik.API_URL)
        config.load()
        config.load(TEST_CONFIG)
        self.assertEqual(config.get('odorik', 'url'), 'https://example.net/')

    def test_argv(self):
        backup = sys.argv
        try:
            sys.argv = ['odorik', 'version']
            output = execute(None)
            self.assertIn('version: {0}'.format(odorik.__version__), output)
        finally:
            sys.argv = backup


class TestInteval(TestCase):
    """Test interval processing"""

    @httpretty.activate
    def test_data_this(self):
        """Test getting data list"""
        register_uris()
        output = execute(['mobile-data', '--this-month'])
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_data_last(self):
        """Test getting data list"""
        register_uris()
        output = execute(['mobile-data', '--last-month'])
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_data_start(self):
        """Test getting data list"""
        register_uris()
        output = execute(['mobile-data', '--start-date', '2015-01-01'])
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_data_start_end(self):
        """Test getting data list"""
        register_uris()
        output = execute([
            'mobile-data',
            '--start-date', '2015-01-01',
            '--end-date', '2015-10-01'
        ])
        self.assertIn('0.15', output)

    def test_data_start_end_wrong(self):
        """Test getting data list"""
        self.assertRaises(
            SystemExit,
            execute,
            [
                'mobile-data',
                '--start-date', '2015-01-01',
                '--end-date', '2015-01-01'
            ]
        )

    def test_data_end(self):
        """Test getting data list"""
        self.assertRaises(
            SystemExit,
            execute,
            ['mobile-data', '--end-date', '2015-01-01']
        )


class TestOutput(TestCase):
    """Test output formatting"""

    def test_version_text(self):
        """Test version printing"""
        output = execute(['--format', 'text', 'version'])
        self.assertIn('version: {0}'.format(odorik.__version__), output)

    def test_version_json(self):
        """Test version printing"""
        output = execute(['--format', 'json', 'version'], True)
        values = json.loads(output)
        self.assertEqual({'version': odorik.__version__}, values)

    def test_version_csv(self):
        """Test version printing"""
        output = execute(['--format', 'csv', 'version'], True)
        self.assertIn('version,{0}'.format(odorik.__version__), output)

    def test_version_html(self):
        """Test version printing"""
        output = execute(['--format', 'html', 'version'])
        self.assertIn(odorik.__version__, output)

    @httpretty.activate
    def test_data_list_text(self):
        """Test getting data list"""
        register_uris()
        output = execute(
            ['--format', 'text', 'mobile-data', '--list']
        )
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_data_list_json(self):
        """Test getting data list"""
        register_uris()
        output = execute(
            ['--format', 'json', 'mobile-data', '--list'],
            True
        )
        values = json.loads(output)
        self.assertEqual(len(values), 1)

    @httpretty.activate
    def test_data_list_csv(self):
        """Test getting data list"""
        register_uris()
        output = execute(
            ['--format', 'csv', 'mobile-data', '--list'],
            True
        )
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_data_list_html(self):
        """Test getting data list"""
        register_uris()
        output = execute(
            ['--format', 'html', 'mobile-data', '--list'],
        )
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_summary_text(self):
        """Test summary for all lines"""
        register_uris()
        output = execute(['--format', 'text', 'summary'])
        self.assertIn('\nprice: 0.15', output)

    @httpretty.activate
    def test_summary_json(self):
        """Test summary for all lines"""
        register_uris()
        output = execute(['--format', 'json', 'summary'], True)
        self.assertIn('"price": 0.1484', output)

    @httpretty.activate
    def test_summary_csv(self):
        """Test summary for all lines"""
        register_uris()
        output = execute(['--format', 'csv', 'summary'], True)
        self.assertIn('\nprice,0.15', output)

    @httpretty.activate
    def test_summary_html(self):
        """Test summary for all lines"""
        register_uris()
        output = execute(['--format', 'html', 'summary'])
        self.assertIn('>price</th><td>0.15<', output)


class TestCommands(TestCase):
    """Test command line interface"""

    def test_version(self):
        """Test version printing"""
        output = execute(['version'])
        self.assertIn(odorik.__version__, output)

    def test_invalid(self):
        """Test invalid command"""
        self.assertRaises(
            SystemExit,
            execute,
            ['invalid']
        )

    def test_version_bare(self):
        """Test version printing"""
        output = execute(['version', '--bare'])
        self.assertTrue(output.startswith(odorik.__version__))

    @httpretty.activate
    def test_balance(self):
        """Test getting balance"""
        register_uris()
        output = execute(['balance'])
        self.assertIn('123.45', output)

    @httpretty.activate
    def test_data_summary(self):
        """Test getting data summary"""
        register_uris()
        output = execute(['mobile-data'])
        self.assertIn('price: 0.15', output)

    @httpretty.activate
    def test_data_number(self):
        """Test getting data summary for number"""
        register_uris()
        output = execute(['mobile-data', '--phone', '00420789123456'])
        self.assertIn('price: 0.15', output)

    @httpretty.activate
    def test_data_all(self):
        """Test getting data summary for number"""
        register_uris()
        output = execute(['mobile-data', '--all'])
        self.assertIn('price: 0.15', output)

    @httpretty.activate
    def test_data_list(self):
        """Test getting data list"""
        register_uris()
        output = execute(['mobile-data', '--list'])
        self.assertIn('0.15', output)

    @httpretty.activate
    def test_calls_summary(self):
        """Test getting calls summary"""
        register_uris()
        output = execute(['calls'])
        self.assertIn('length: 362', output)

    @httpretty.activate
    def test_calls_list(self):
        """Test getting calls list"""
        register_uris()
        output = execute(['calls', '--list'])
        self.assertIn('554.03', output)

    @httpretty.activate
    def test_calls_line(self):
        """Test getting calls summary for line"""
        register_uris()
        output = execute(['calls', '--line', '1234'])
        self.assertIn('length: 362', output)

    @httpretty.activate
    def test_sms_summary(self):
        """Test getting sms summary"""
        register_uris()
        output = execute(['sms'])
        self.assertIn('price: 0.0', output)

    @httpretty.activate
    def test_sms_list(self):
        """Test getting sms list"""
        register_uris()
        output = execute(['sms', '--list'])
        self.assertIn('direction: in', output)

    @httpretty.activate
    def test_sms_line(self):
        """Test getting sms summary for line"""
        register_uris()
        output = execute(['sms', '--line', '1234'])
        self.assertIn('price: 0.0', output)

    @httpretty.activate
    def test_send_sms(self):
        """Test sending SMS"""
        register_uris()
        output = execute([
            'send-sms',
            '00420789123456',
            'text'
        ])
        self.assertEquals('', output)

    @httpretty.activate
    def test_send_sms_invalid(self):
        """Test sending SMS"""
        register_uris()
        self.assertRaises(
            SystemExit,
            execute,
            ['send-sms', 'INVALID', 'text'],
        )

    @httpretty.activate
    def test_callback(self):
        """Test callback"""
        register_uris()
        output = execute([
            'callback', '00420789123456', '800123456'
        ])
        self.assertEquals('', output)

    @httpretty.activate
    def test_summary(self):
        """Test summary for all lines"""
        register_uris()
        output = execute(['summary'])
        self.assertIn('\nprice: 0.15', output)

    @httpretty.activate
    def test_lines(self):
        """Test lines"""
        register_uris()
        output = execute(['lines'])
        self.assertIn('active_822', output)

    @httpretty.activate
    def test_lines_config(self):
        """Test lines generating config"""
        register_uris()
        output = execute(['lines', '--generate-config'])
        self.assertIn('Test = 123465', output)


class TestAPI(TestCase):
    """Test generic API support"""

    @httpretty.activate
    def test_api(self):
        """Test API GET operation"""
        register_uris()
        output = execute(['api', 'sms/allowed_sender'])
        self.assertIn('Odorik.cz,5517,00420789123456', output)

    @httpretty.activate
    def test_api_params(self):
        """Test API GET params operation"""
        register_uris()
        output = execute([
            'api', 'calls.json',
            '--param', 'from=2015-05-01T00:00:00+02:00',
            '--param', 'to=2015-05-18T00:00:00+02:00'
        ])
        self.assertIn('*300000', output)

    @httpretty.activate
    def test_api_wrong(self):
        """Test API wrong params operation"""
        register_uris()
        self.assertRaises(
            SystemExit,
            execute,
            [
                'api', 'calls.json',
                '--param', 'from',
            ],
        )

    @httpretty.activate
    def test_api_post(self):
        """Test API POST operation"""
        register_uris()
        output = execute([
            'api', 'callback', '--post',
            '--param', 'caller=00420789123456',
            '--param', 'recipient=800123456'
        ])
        self.assertIn('callback_ordered', output)
