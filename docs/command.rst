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

.. option:: version

    Prints current version.

.. option:: balance

    Prints current balance.

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
