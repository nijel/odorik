:mod:`odorik`
=============

.. module:: odorik
    :synopsis: Odorik API


.. exception:: OdorikException

    Base class for all exceptions.


:class:`Odorik`
---------------

.. class:: Odorik(user, password, url=None)

    :param user: User ID
    :type user: string
    :param password: API password
    :type password: string
    :param url: API server URL, if not specified default is used
    :type url: string

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
