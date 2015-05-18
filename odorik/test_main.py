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
from odorik.test_odorik import register_uris


class TestCommands(TestCase):
    """Test command line interface"""
    @staticmethod
    def execute(args, binary=False, settings=None):
        """Execute command and return output."""
        if settings is None:
            settings = ()
        elif not settings:
            settings = None
        if binary and sys.version_info < (3, 0):
            output = BytesIO()
        else:
            output = StringIO()
        main(args=args, stdout=output, settings=settings)
        return output.getvalue()

    def test_version(self):
        """Test version printing"""
        output = self.execute(['version'])
        self.assertTrue(odorik.__version__ in output)

    def test_invalid(self):
        """Test invalid command"""
        self.assertRaises(
            SystemExit,
            self.execute,
            ['invalid']
        )

    def test_version_json(self):
        """Test version printing"""
        output = self.execute(['--format', 'json', 'version'], True)
        values = json.loads(output)
        self.assertEqual({'version': odorik.__version__}, values)

    def test_version_csv(self):
        """Test version printing"""
        output = self.execute(['--format', 'csv', 'version'], True)
        self.assertTrue('version,{0}'.format(odorik.__version__) in output)

    def test_version_bare(self):
        """Test version printing"""
        output = self.execute(['version', '--bare'])
        self.assertTrue(output.startswith(odorik.__version__))

    @httpretty.activate
    def test_balance(self):
        """Test getting balance"""
        register_uris()
        output = self.execute(['balance'])
        self.assertTrue('123.45' in output)

    @httpretty.activate
    def test_balance_api(self):
        """Test getting balance using different API"""
        register_uris()
        output = self.execute(['--url', 'https://example.net/', 'balance'])
        self.assertTrue('321.09' in output)

    @httpretty.activate
    def test_settings(self):
        register_uris()
        output = self.execute(
            ['balance'],
            settings=(('odorik', 'url', 'https://example.net/'),)
        )
        self.assertTrue('321.09' in output)


    @httpretty.activate
    def test_config(self):
        register_uris()
        config = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'odorik'
        )
        output = self.execute(['--config', config, 'balance'], settings=False)
        self.assertTrue('321.09' in output)

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
        output = self.execute(['mobile-data', '--phone', '00420789123456'])
        self.assertTrue('price: 0.1484' in output)

    @httpretty.activate
    def test_data_list(self):
        """Test getting data list"""
        register_uris()
        output = self.execute(['mobile-data', '--list'])
        self.assertTrue('0.1484' in output)

    @httpretty.activate
    def test_data_list_json(self):
        """Test getting data list"""
        register_uris()
        output = self.execute(
            ['--format', 'json', 'mobile-data', '--list'],
            True
        )
        values = json.loads(output)
        self.assertEqual(len(values), 1)

    @httpretty.activate
    def test_data_list_csv(self):
        """Test getting data list"""
        register_uris()
        output = self.execute(
            ['--format', 'csv', 'mobile-data', '--list'],
            True
        )
        self.assertTrue('0.1484' in output)

    @httpretty.activate
    def test_api(self):
        """Test API GET operation"""
        register_uris()
        output = self.execute(['api', 'sms/allowed_sender'])
        self.assertTrue('Odorik.cz,5517,00420789123456' in output)

    @httpretty.activate
    def test_api_params(self):
        """Test API GET params operation"""
        register_uris()
        output = self.execute([
            'api', 'calls.json',
            '--param', 'from=2015-05-01T00:00:00+02:00',
            '--param', 'to=2015-05-18T00:00:00+02:00'
        ])
        self.assertTrue('*300000' in output)

    @httpretty.activate
    def test_api_wrong(self):
        """Test API wrong params operation"""
        register_uris()
        self.assertRaises(
            SystemExit,
            self.execute,
            [
                'api', 'calls.json',
                '--param', 'from',
            ],
        )

    @httpretty.activate
    def test_api_post(self):
        """Test API POST operation"""
        register_uris()
        output = self.execute([
            'api', 'callback', '--post',
            '--param', 'caller=00420789123456',
            '--param', 'recipient=800123456'
        ])
        self.assertTrue('callback_ordered' in output)

    @httpretty.activate
    def test_send_sms(self):
        """Test sending SMS"""
        register_uris()
        output = self.execute([
            'send-sms',
            '00420789123456',
            'text'
        ])
        self.assertEquals('', output)

    @httpretty.activate
    def test_callback(self):
        """Test callback"""
        register_uris()
        output = self.execute([
            'callback', '00420789123456', '800123456'
        ])
        self.assertEquals('', output)
