Python API
~~~~~~~~~~

:mod:`odorik`
=============

.. module:: odorik
    :synopsis: Odorik API

:exc:`OdorikException`
----------------------

.. exception:: OdorikException

    Base class for all exceptions.


:class:`Odorik`
---------------

.. class:: Odorik(user='', password='', url=None, config=None, section='odorik'):

    :param user: User ID
    :type user: string
    :param password: API password
    :type password: string
    :param url: API server URL, if not specified default is used
    :type url: string
    :param config: Configuration object, overrides any other parameters.
    :type config: OdorikConfig

    Access class to the API, define user, password and optionally API URL.

    .. method:: get(path, args=None)

        :param path: Request path
        :type path: string
        :param args: Optional request parameters
        :type args: dict
        :rtype: string

        Performs single API GET call.

    .. method:: get_json(path, args=None)

        :param path: Request path
        :type path: string
        :param args: Optional request parameters
        :type args: dict
        :rtype: object

        Performs single API GET call and parses JSON reply including error
        handling.

    .. method:: balance()

        :rtype: float

        Returns current balance.

    .. method:: mobile_data(from_date, to_date, number=None)

        :param from_date: Starting date
        :type from_date: datetime.datetime
        :param to_date: Ending date
        :type to_date: datetime.datetime
        :param number: Phone number in form of 00420789123456
        :type number: string
        :rtype: list

        Returns mobile data usage list in given interval. Optionally filtered
        for given number.

    .. method:: send_sms(recipient, message, sender='5517')

        :param recipient: Number where to sent SMS.
        :type recipient: string
        :param message: Text of the message.
        :type message: string
        :param sender: Optional sender number.
        :type sender: string
        :rtype: string

        Sends a SMS message.

    .. method:: callback(caller, recipient, line=None)

        :param caller: Number which is calling.
        :type caller: string
        :param recipient: Number to call.
        :type recipient: string
        :param line: Line to use for accounting.
        :type line: string or None
        :rtype: string

        Initiates callback.

    .. method:: calls(from_date, to_date, line=None):

        :param from_date: Starting date
        :type from_date: datetime.datetime
        :param to_date: Ending date
        :type to_date: datetime.datetime
        :param line: Line to use for listing
        :type line: string or None
        :rtype: list

        Returns list of calls in given interval. Optionally filtered for given
        line.

    .. method:: sms(from_date, to_date, line=None):

        :param from_date: Starting date
        :type from_date: datetime.datetime
        :param to_date: Ending date
        :type to_date: datetime.datetime
        :param line: Line to use for listing
        :type line: string or None
        :rtype: list

        Returns list of sms in given interval. Optionally filtered for given
        line.

    .. method:: lines()

        :rtype: list

        Returns list of dictionaries with information about lines.


:mod:`odorik.config`
====================

.. module:: odorik.config
    :synopsis: Configuration parsing

:class:`OdorikConfig`
---------------------

.. class:: OdorikConfig(section='odorik')
    
    :param section: Configuration section to use
    :type section: string

    Configuration file parser following XDG specification.


    .. method:: load(path=None)

        :param path: Path where to load configuration.
        :type path: string

        Loads configuration from a file, if none is specified it loads from
        `odorik` configuration file placed in XDG configuration path
        (:file:`~/.config/odorik` and :file:`/etc/xdg/odorik`).


:mod:`odorik.main`
==================

.. module:: odorik.main
    :synopsis: Command line interface

.. function:: main(settings=None, stdout=None, args=None)

    :param settings: settings to override
    :type settings: list of tuples
    :param stdout: stdout for printing output, uses ``sys.stdout`` as default
    :type stdout: file
    :param args: command line argumets to process, uses ``sys.args`` as default
    :type args: list

    Main entry point for command line interface.

.. decorator:: register_command(command)

    Decorator to register :class:`Command` class in main parser used by
    :func:`main`.

:class:`Command`
----------------

.. class:: Command(args, config, stdout=None)

    Main class for invoking commands.
