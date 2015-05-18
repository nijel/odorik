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
easily access some of the functionality from command line. Currently following
subcommands are available:

.. option:: --format {csv,json,text}

    Specify output format.

.. option:: --url URL

    Specify API URL. Overrides value from configuration file, see :ref:`files`.

.. option:: --user USER

    Specify API user. Overrides value from configuration file, see :ref:`files`.

.. option:: --password PASSWORD

    Specify API password. Overrides value from configuration file, see :ref:`files`.

.. option:: --config PATH

    Override path to configuration file, see :ref:`files`.

.. option:: version

    Prints current version.

.. option:: api PATH [--post] [--param KEY=VALUE]...

    Performs authenticated API call.

.. option:: balance

    Prints current balance.

.. option:: mobile-data [--list] [--phone NUMBER]

    Prints mobile data usage.

    It can list all individual records.

    The result can be also limited to given phone number. Needs to be specified
    as ``00420789123456``.

.. option:: send-sms [--sender SENDER] recipient message

    Sends a SMS message.

.. _files:

Files
+++++

~/.config/odorik
    User configuration file
/etc/xdg/odorik
    Global configration file

The program follows XDG specification, so you can adjust placement of config files
by environment variables ``XDG_CONFIG_HOME`` or ``XDG_CONFIG_DIRS``.

Following settings can be configured in the ``[odorik]`` section:

.. describe:: user

    API user, can be either ID registered user or line ID.

.. describe:: password

    API password. Use API password for per user access and line password (used
    for SIP as well) for line access.

.. describe:: url

    API server URL, defaults to ``https://www.odorik.cz/api/v1/``.

The configuration file is INI file, for example:

.. code-block:: ini

    [odorik]
    user = pepa
    password = zdepa

.. seealso:: http://www.odorik.cz/w/api#autentizace

Examples
++++++++

Print current program version:

.. code-block:: sh

    $ odorik version
    0.1

Print current user balance:

.. code-block:: sh

    $ odorik balance
    123.45

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
