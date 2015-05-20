Odorik command line interface
=============================

.. program:: odorik

Synopsis
++++++++

.. code-block:: text

    odorik [parameter] <command> [options]

Commands actually indicate which operation should be performed.

Description
+++++++++++

This module also installs :program:`odorik` program, which allows you to
easily access some of the functionality from command line.

Global options
--------------

The program accepts following global options, which must be entered before subcommand.

.. option:: --format {csv,json,text,html}

    Specify output format.

.. option:: --url URL

    Specify API URL. Overrides value from configuration file, see :ref:`files`.

.. option:: --user USER

    Specify API user. Overrides value from configuration file, see :ref:`files`.

.. option:: --password PASSWORD

    Specify API password. Overrides value from configuration file, see :ref:`files`.

.. option:: --config PATH

    Override path to configuration file, see :ref:`files`.

.. option:: --config-section SECTION

    Override section to use in configuration file, see :ref:`files`.

Subcommands
-----------

Currently following subcommands are available:

.. option:: version

    Prints current version.

.. option:: api PATH [--post] [--param KEY=VALUE]...

    Performs authenticated API call. By default ``GET`` method is used, with
    ``--post`` it is ``POST``.

    Additional parameters can be specified by ``--param`` switch which can be
    used multiple times.

.. option:: balance

    Prints current balance.

.. option:: mobile-data [--list] [--phone NUMBER] [--all] [DATE PERIOD]

    Prints mobile data usage.

    It can list all individual records when ``--list`` is specified.

    The result can be also limited to given phone number by using ``--phone``.
    The phone number has to be specified as ``00420789123456``.

    If ``--all`` is specified, summary for all mobile lines on current account
    is printed.

    See :ref:`interval` for information how to specify date period.

.. option:: calls [--list] [--line LINE] [DATE PERIOD]

    Prints calls usage.

    It can list all individual records when ``--list`` is specified.

    The result can be also limited to given line by using ``--line``.

    See :ref:`interval` for information how to specify date period.

.. option:: sms [--list] [--line LINE] [DATE PERIOD]

    Prints SMS usage.

    It can list all individual records when ``--list`` is specified.

    The result can be also limited to given line by using ``--line``.

    See :ref:`interval` for information how to specify date period.

.. option:: send-sms [--sender SENDER] recipient message

    Sends a SMS message.

    You can specify sender number by ``--sender``, it has to be one of allowed
    values. By default ``5517`` is used.

.. option:: callback [--line LINE] caller recipient

    Initiates a callback.

.. option:: lines [--generate-config]

    Prints infromation about lines.

    With ``--generate-config`` it generates config file entries for line and
    phone number aliases, see :ref:`files`.

.. option:: summary [DATE PERIOD]

    Prints summary information for all lines in current account.

    See :ref:`interval` for information how to specify date period.

.. _interval:

Specifying date period
----------------------

You can specify date period for which many commands will be issued:

.. option:: --this-month

    Prints information for current month. This is the default interval.

.. option:: --last-month

    Prints information for last month.

.. option:: --start-date DATE

    Starting datetime.

.. option:: --end-date DATE

    Ending datetime. If not specified, current date is used.

All parameters accepting date can take almost any format of date or timestamp.
Check `dateutil <http://labix.org/python-dateutil#head-b95ce2094d189a89f80f5ae52a05b4ab7b41af47>`_
documentation for more detailed information (especially on year/month/day
precendence).

.. _files:

Files
+++++

:file:`~/.config/odorik`
    User configuration file
:file:`/etc/xdg/odorik`
    Global configration file

The program follows XDG specification, so you can adjust placement of config files
by environment variables ``XDG_CONFIG_HOME`` or ``XDG_CONFIG_DIRS``.

Following settings can be configured in the ``[odorik]`` section (you can
customize this by :option:`--config-option`):

.. describe:: user

    API user, can be either ID registered user or line ID.

.. describe:: password

    API password. Use API password for per user access and line password (used
    for SIP as well) for line access.

.. describe:: url

    API server URL, defaults to ``https://www.odorik.cz/api/v1/``.

See `Autentizace Odorik API <http://www.odorik.cz/w/api#autentizace>`_ for more
details on authentication.

The configuration file is INI file, for example:

.. code-block:: ini

    [odorik]
    user = pepa
    password = zdepa

Additionally config file can include phone number and line aliases:

.. code-block:: ini

    [lines]
    pepa = 12345

    [numbers]
    pepa = 00420789789789
    franta = 00420789123456

Examples
++++++++

Print current program version:

.. code-block:: sh

    $ odorik version
    version: 0.1

Print current user balance:

.. code-block:: sh

    $ odorik balance
    balance: 123.45

Prints current mobile data usage:

.. code-block:: sh

    $ odorik mobile-data --phone 00420789123456
    bytes_total: 111593707
    bytes_down: 87039672
    bytes_up: 24554035
    price: 0

Sending message:

.. code-block:: sh

    $ odorik send-sms 00420789123456 "Ahoj, jak se mas?"

Initiating callback:

.. code-block:: sh

    $ odorik callback 00420789123456 800123456

Getting account summary:

.. code-block:: sh

    $ odorik summary
    Pepa
    id: 716000
    public_number: 00420789789789
    call_count: 58
    sms_count: 42
    bytes_total: 145921813
    data_price: 0.01
    call_price: 24.28
    sms_price: 12.31
    price: 36.59

    Franta
    id: 717000
    public_number: 00420789123456
    call_count: 11
    sms_count: 0
    bytes_total: 0
    data_price: 0
    call_price: 2.20
    sms_price: 0
    price: 2.20

Generic API usage:

.. code-block:: sh

    $ odorik api sms/allowed_sender
    Odorik.cz,5517,00420789123456

Generic API POST:

.. code-block:: sh

    $ odorik api --post --param caller=00420789123456 --param recipient=800123456 callback

Machine readable output formats:

.. code-block:: sh

    $ odorik --format json mobile-data
    {
      "bytes_total": 111593707,
      "bytes_down": 87039672,
      "bytes_up": 24554035,
      "price": 0.008
    }
    $ odorik --format csv mobile-data
    bytes_total,111593707
    bytes_down,87039672
    bytes_up,24554035
    price,0.008
