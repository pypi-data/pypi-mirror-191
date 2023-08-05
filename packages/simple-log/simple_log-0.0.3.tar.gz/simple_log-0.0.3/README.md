Simple Logging
===============================

* version number: 0.0.3
* date: 2023.02.10
* author: Andrew J. Todd esq.

Overview
--------

A python module to allow you to log with minimal fuss. It's a wrapper around the standard logging module with sensible defaults and as little configuration as possible. Documentation is on [halfcooked.com](https://halfcooked.com/code/simple_log/)

Installation 
------------

To install use pip:

    $ pip install simple_log


Or clone the repo:

    $ hg clone https://hg.sr.ht/~andy47/simple_log
    $ python setup.py install
    
Usage
-----

We try and stay true to the name and make using this module as simple as possible. For the simplest case just use

    >>> from simple_log import get_log
    >>> my_log = get_log()
    >>> my_log.info("This is an information message")
    2016.11.10 22:21:51 default INFO:: This is an information message
    
If you want to have multiple logs just pass a name to `get_log`

    >>> first_log = get_log("first")
    >>> first_log.info("Information message to first log")
    2016.11.10 22:27:30 first INFO:: Information message to first log
    >>> second_log = get_log("two")
    >>> second_log.debug("This is a debug message")
    2016.11.10 22:28:02 two DEBUG:: This is a debug message

By default the logging level is set to `'INFO'` (the standard module defaults to `'WARNING'`). See the [logging tutorial](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) for information on logging levels. If you would like to change the logging level, for instance to display 'DEBUG' messages use the `setLevel` method on your log object

    >>> from simple_log import get_log
    >>> my_log = get_log('test_log')
    >>> my_log.debug('This is the first debug message')
    ...
    >>> my_log.setLevel('DEBUG')
    >>> my_log.debug('This is the second debug message')
    2016.11.10 22:34:55 test_log DEBUG:: This is the second debug message

The log level values that you can pass to `setLevel` are `'DEBUG'`, `'INFO'` (the default), `'WARNING'`, `'ERROR'` or `'CRITICAL'`.

If you would like your log messages written to a file as well as the screen use the `add_file` function

    >>> from simple_log import get_log, add_file
    >>> my_log = get_log('test_log')
    >>> my_log.info('This is an information message')
    2016.11.12 22:48:10 test_log INFO:: This is an information message
    >>> add_file('test_log', 'test_log.log')
    >>> my_log.info('This is another information message')
    2016.11.12 22:49:30 test_log INFO:: This is another information message
    >>> cat test_log.log
    2016.11.12 22:49:30 test_log INFO:: This is another information message
    
Contributing
------------

If you would like to contribute please visit the project web site at - https://hg.sr.ht/~andy47/simple_log
