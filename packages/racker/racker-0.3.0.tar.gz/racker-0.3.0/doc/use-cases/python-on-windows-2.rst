##########################
Python packages on Windows
##########################


*****
About
*****

Python packages are not always compatible with Windows out of the box.
Racker can assist you to find out why.


********
Projects
********

We had a look at some projects from our pen and discovered that not a single
one even installs successfully on Windows.


Wetterdienst
============

Coming from ``pip install wetterdienst``::

    racker --verbose run --rm --platform=windows/amd64 python:3.9-windowsservercore -- pip install "measurement<4.0,>=3.2"

::

    FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\ContainerAdministrator\\AppData\\Local\\Temp\\pip-install-4n5faa8m\\measurement_025b7dbbe1da4059871522586272b150\\.eggs\\sphinxcontrib_serializinghtml-1.1.5-py3.9.egg\\sphinxcontrib\\serializinghtml\\locales\\sr@latin\\LC_MESSAGES\\sphinxcontrib.serializinghtml.mo'
    [end of output]

See also https://github.com/coddingtonbear/python-measurement/issues/70#issuecomment-1152939348.


PyTables
========

Coming from ``pip install tables``::

    racker --verbose run --rm --platform=windows/amd64 python:3.9 -- 'sh -c "pip install numexpr; python -c \"import numexpr\""'

::

    >>> import numexpr
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Python\lib\site-packages\numexpr\__init__.py", line 24, in <module>
        from numexpr.interpreter import MAX_THREADS, use_vml, __BLOCK_SIZE1__
    ImportError: DLL load failed while importing interpreter: The specified module could not be found.

See also https://github.com/pydata/numexpr/issues/372.


Kotori
======

Coming from ``pip install kotori``::

    racker --verbose run --rm --platform=windows/amd64 python:3.9 -- pip install Twisted[tls]==20.3.0
::

    Building wheels for collected packages: Twisted
      Building wheel for Twisted (setup.py): started
      Building wheel for Twisted (setup.py): finished with status 'error'
      error: subprocess-exited-with-error

      building 'twisted.test.raiser' extension
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]


PatZilla
========

Coming from ``pip install patzilla``::

    racker --verbose run --rm --platform=windows/amd64 python:2.7 -- pip install pycrypto

::

    Collecting pycrypto
      Downloading pycrypto-2.6.1.tar.gz (446 kB)
    Building wheels for collected packages: pycrypto
      Building wheel for pycrypto (setup.py): started
      Building wheel for pycrypto (setup.py): finished with status 'error'
      ERROR: Command errored out with exit status 1:
      warning: GMP or MPIR library not found; Not building Crypto.PublicKey._fastmath.
      building 'Crypto.Random.OSRNG.winrandom' extension
      error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27


NumPy
=====

Needs build environment::

    racker --verbose run --rm --platform=windows/amd64 python:3.11-rc -- 'sh -c "pip install numpy; python -c \"import numpy; numpy.show_config()\""'

::

    Building wheels for collected packages: numpy
      Building wheel for numpy (pyproject.toml): started
      Building wheel for numpy (pyproject.toml): finished with status 'error'
      error: subprocess-exited-with-error

      × Building wheel for numpy (pyproject.toml) did not run successfully.

      INFO: building library "npymath" sources
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]


mqttwarn
========
::

    racker --verbose run --rm --platform=windows/amd64 python:3.9 -- 'sh -c "pip install mqttwarn; mqttwarn --version"'
    racker --verbose run --rm --platform=windows/amd64 python:3.9 -- 'sh -c "pip install mqttwarn; python -c \"import mqttwarn\""'
