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
"""Test the module."""
from __future__ import unicode_literals

from unittest import TestCase
from odorik import Odorik, OdorikException
from decimal import Decimal
import httpretty
import datetime
try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


DATA_BODY = (
    '[{"id":133,"date":"2013-07-11T14:43:59Z","bytes_up":151666,' +
    '"bytes_down":3768,"bytes_total":155434,"price":0.1484,' +
    '"price_per_mb":1.0,"phone_number":"00420799799799"}]'
)


def sms_response(request, uri, headers):
    """httpretty SMS sending response generator"""
    params = parse_qs(request.body)
    print(uri, request.body, params)
    if params['sender'][0] == '5517':
        return (200, headers, 'successfully_sent 132.44')
    return (200, headers, 'error unsupported_recipient')


def register_uris():
    """Register URIs for httpretty."""
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/balance',
        body='123.45'
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/sim_cards/mobile_data.json',
        body=DATA_BODY
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/sim_cards/'
        '00420789123456/mobile_data.json',
        body=DATA_BODY
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/sim_cards/INVALID/mobile_data.json',
        body='{"errors":["nonexisting_public_number"]}'
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/sms/allowed_sender',
        body='Odorik.cz,5517,00420789123456'
    )
    httpretty.register_uri(
        httpretty.POST,
        'https://www.odorik.cz/api/v1/sms',
        body=sms_response,
    )


class OdorikTest(TestCase):
    """Testing of Odorik class"""
    @httpretty.activate
    def test_balance(self):
        """Test getting balance"""
        register_uris()
        self.assertEqual(
            Odorik().balance(),
            Decimal('123.45')
        )

    @httpretty.activate
    def test_data(self):
        """Test getting balance"""
        register_uris()
        self.assertEqual(
            len(Odorik().mobile_data(
                datetime.datetime.now(),
                datetime.datetime.now(),
            )),
            1
        )

    @httpretty.activate
    def test_data_number(self):
        """Test getting balance"""
        register_uris()
        self.assertEqual(
            len(Odorik().mobile_data(
                datetime.datetime.now(),
                datetime.datetime.now(),
                '00420789123456'
            )),
            1
        )

    @httpretty.activate
    def test_data_invalid(self):
        """Test getting balance"""
        register_uris()
        self.assertRaises(
            OdorikException,
            Odorik().mobile_data,
            datetime.datetime.now(),
            datetime.datetime.now(),
            'INVALID'
        )

    @httpretty.activate
    def test_sms(self):
        """Test sending SMS"""
        register_uris()
        self.assertEquals(
            Odorik().send_sms(
                '00420789123456',
                'text'
            ),
            'successfully_sent 132.44'
        )

    @httpretty.activate
    def test_sms_invalid(self):
        """Test sending SMS"""
        register_uris()
        self.assertRaises(
            OdorikException,
            Odorik().send_sms,
            '00420789123456',
            'text',
            '123456',
        )
