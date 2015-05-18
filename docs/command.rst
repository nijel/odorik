Odorik command line interface
=============================

.. program:: odorik

Synopsis
++++++++

.. code-block:: text

    odorik <command> [options]

Commands actually indicate which operation should be performed.

Description
+++++++++++

This module also installs :program:`odorik` program, which allows you to
easily access some of the functionality from command line. Currently following
subcommands are available:

.. option:: --format [csv|json|text]

    Specify output format.

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

Files
+++++

~/.config/odorik
    User configuration file
/etc/xdg/odorik
    Global configration file

The program follows XDG specification, so you can adjust placement of config files 
by environment variables ``XDG_CONFIG_HOME`` or ``XDG_CONFIG_DIRS``.

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
