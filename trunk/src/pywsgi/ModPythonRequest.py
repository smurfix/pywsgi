# Copyright (C) 2008 Samuel Abels, http://debain.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import cgi
from Request import Request

class ModPythonRequest(Request):
    def __init__(self, request, **kwargs):
        from mod_python      import apache, Cookie
        from mod_python.util import FieldStorage
        Request.__init__(self, **kwargs)
        self.request   = request
        self.env       = apache.build_cgi_env(request)
        self.get_data  = cgi.parse_qs(self.get_env('QUERY_STRING'))
        self.post_data = self.__unpack_data(request.form)
        self.cookies   = self.__unpack_data(Cookie.get_cookies(request))


    def get_name(self):
        return 'mod_python'


    def __unpack_data(self, data):
        result = {}
        for key, field in data.items():
            result[key] = [field.value]
        return result


    def get_env(self, key):
        return self.env[key]


    def has_get_data(self, key, value = None):
        if value is None:
            return self.get_data.has_key(key)
        return self.get_data.get(key) == value


    def get_get_data(self, key = None, default = None):
        if key is None:
            return self.get_data
        return self.get_data.get(key, default)


    def has_post_data(self, key = None, value = None):
        if key is None:
            return self.request.method == 'POST'
        if value is None:
            self.post_data.has_key(key)
        return self.post_data.get(key) == value


    def get_post_data(self, key = None, default = None):
        if key is None:
            return self.post_data
        return self.post_data.get(key, default)


    def set_cookie(self, key, value, expires = None):
        cookie = Cookie.Cookie(key, value)
        if expires:
            cookie.expires = expires
        Cookie.add_cookie(self.request, cookie)


    def get_cookie(self, key = None, default = None):
        if key is None:
            return self.cookies
        return self.cookies.get(key, default)


    def add_header(self, key, value):
        return self.headers_out.add(key, value)


    def get_headers(self):
        return self.headers_out.items()


    def flush(self):
        self.request.content_type = self.content_type
        self.request.write(self.data)
        data = self.data
        self.data = ''
        return [data]


    def handle_exception(self):
        raise


    def handle(self, func):
        func(self)
        self.flush()
