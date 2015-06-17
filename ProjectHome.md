pywsgi is a Python module that abstracts from CGI, WSGI, and mod\_python.

**What pywsgi is:**

  * An abstraction from low-level gateway interface handlers like WSGI, CGI, and mod\_python.
  * A consistent high-level, class-based interface.
  * Session handling.
  * Cookie handling.
  * GET/POST data handling.
  * Error handling.
  * A pywsgi.util namespace with useful tools.

**What pywsgi is not:**
  * An official Python project. There is no official high-level WSGI API in Python.
  * A Python implementation of the WSGI specification. Instead, this module wraps the exising low-level Python implementation (which is named wsgiref).