from setuptools import setup, find_packages
setup(name             = 'pywsgi',
      version          = '0.9.0',
      description      = 'A high-level class-based API around WSGI, CGI, and mod_python',
      long_description = \
"""
What pywsgi is:

  - An abstraction from low-level gateway interface handlers like WSGI,
    CGI, and mod_python.
  - A consistent high-level, class-based interface.
  - Session handling.
  - Cookie handling.
  - GET/POST data handling.
  - Error handling.
  - A pywsgi.util namespace with useful tools.

What pywsgi is not:

  - An official Python project.
  - A Python implementation of the WSGI specification. Instead, this module
    wraps the exising low-level Python implementation (which is named
    wsgiref).
""",
      author           = 'Samuel Abels',
      author_email     = 'cheeseshop.python.org@debain.org',
      license          = 'GPLv2',
      package_dir      = {'': 'src'},
      packages         = ['pywsgi', 'pywsgi.util'],
      install_requires = [],
      keywords         = 'pywsgi web cgi wsgi mod_python adapter bridge url',
      url              = 'http://code.google.com/p/pywsgi/',
      classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ])
