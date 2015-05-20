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

CALLS_BODY = (
    '[{"id": 98292358,"redirection_parent_id": 98292356, '
    '"date": "2014-10-01T11:28:31Z", "direction": "redirected", '
    '"source_number": "00420555444333", "destination_number": "*300000", '
    '"destination_name": "Česká rep. - * v síti", "length": 362, '
    '"ringing_length": 8, "status": "answered", "price": 0.0, '
    '"price_per_minute": 0.0, "balance_after": 554.0288, '
    '"line": 403366}]'
)

SMS_BODY = ('''[
      {
        "status": "unknown",
        "direction": "in",
        "destination_number": "00420799799799",
        "line": 716000,
        "price": 0.0,
        "source_number": "00420799799799",
        "date": "2015-05-18T16:26:56Z",
        "balance_after": 377.7841,
        "type": "sms",
        "id": 121250000
      }
    ]
''')

LINES_BODY = (
    '[ { "incoming_call_name_format": 0, "active_pin": true, '
    '"active_anonymous": true, "id": 123465, "active_greeting": false, '
    '"connected_devices": [], "missed_call_email": "noreply@example.net", '
    '"recording_email": "noreply@example.net", "sip_password": "65432109", '
    '"active_password": true, "public_number": "00420799799799", '
    '"active_cz_restriction": false, "active_iax": false, '
    '"caller_id": "00420799799799", "active_ping": false, '
    '"backup_number": null, "incoming_call_number_format": 0, '
    '"name": "Test", "active_sip": true, "active_rtp": false, '
    '"backup_number_email": null, '
    '"voicemail_email": "noreply@example.net", "active_822": false}]'
)


def sms_response(request, uri, headers):
    """httpretty SMS sending response generator."""
    assert uri.endswith('/sms')
    params = parse_qs(request.body.decode('utf-8'))
    if params['sender'][0] == '5517':
        return (200, headers, 'successfully_sent 132.44')
    return (200, headers, 'error unsupported_recipient')


def register_uris():
    """Register URIs for httpretty."""
    httpretty.register_uri(
        httpretty.GET,
        'https://example.net/balance',
        body='321.09'
    )
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
        'https://www.odorik.cz/api/v1/sim_cards/'
        '00420799799799/mobile_data.json',
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
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/calls.json',
        body=CALLS_BODY
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/sms.json',
        body=SMS_BODY
    )
    httpretty.register_uri(
        httpretty.GET,
        'https://www.odorik.cz/api/v1/lines.json',
        body=LINES_BODY
    )
    httpretty.register_uri(
        httpretty.POST,
        'https://www.odorik.cz/api/v1/callback',
        body='callback_ordered'
    )


class OdorikTest(TestCase):
    """Testing of Odorik class."""
    @httpretty.activate
    def test_balance(self):
        """Test getting balance."""
        register_uris()
        self.assertAlmostEqual(
            Odorik().balance(),
            123.45
        )

    @httpretty.activate
    def test_data(self):
        """Test getting balance."""
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
        """Test getting balance."""
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
        """Test getting balance."""
        register_uris()
        self.assertRaises(
            OdorikException,
            Odorik().mobile_data,
            datetime.datetime.now(),
            datetime.datetime.now(),
            'INVALID'
        )

    @httpretty.activate
    def test_sms_send(self):
        """Test sending SMS."""
        register_uris()
        self.assertEquals(
            Odorik().send_sms(
                '00420789123456',
                'text'
            ),
            'successfully_sent 132.44'
        )

    @httpretty.activate
    def test_sms_send_invalid(self):
        """Test sending SMS."""
        register_uris()
        self.assertRaises(
            OdorikException,
            Odorik().send_sms,
            '00420789123456',
            'text',
            '123456',
        )

    @httpretty.activate
    def test_callback(self):
        """Test callback."""
        register_uris()
        self.assertEquals(
            Odorik().callback(
                '00420789123456',
                '800123456'
            ),
            'callback_ordered'
        )

    @httpretty.activate
    def test_callback_line(self):
        """Test callback."""
        register_uris()
        self.assertEquals(
            Odorik().callback(
                '00420789123456',
                '800123456',
                '123'
            ),
            'callback_ordered'
        )

    @httpretty.activate
    def test_calls(self):
        """Test calls."""
        register_uris()
        self.assertEquals(
            len(Odorik().calls(
                datetime.datetime.now(),
                datetime.datetime.now(),
            )),
            1
        )

    @httpretty.activate
    def test_calls_line(self):
        """Test calls."""
        register_uris()
        self.assertEquals(
            len(Odorik().calls(
                datetime.datetime.now(),
                datetime.datetime.now(),
                '123'
            )),
            1
        )

    @httpretty.activate
    def test_sms(self):
        """Test sms."""
        register_uris()
        self.assertEquals(
            len(Odorik().sms(
                datetime.datetime.now(),
                datetime.datetime.now(),
            )),
            1
        )

    @httpretty.activate
    def test_sms_line(self):
        """Test sms."""
        register_uris()
        self.assertEquals(
            len(Odorik().sms(
                datetime.datetime.now(),
                datetime.datetime.now(),
                '123'
            )),
            1
        )

    @httpretty.activate
    def test_lines(self):
        """Test getting lines information."""
        register_uris()
        self.assertEqual(
            len(Odorik().lines()),
            1
        )
