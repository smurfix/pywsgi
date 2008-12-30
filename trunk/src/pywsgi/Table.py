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

class Table(object):
    def __init__(self, init = None, allow_duplicates = True):
        self.allow_duplicates = allow_duplicates
        self.data_dict        = {}
        if init is None:
            self.data_list = []
        elif isinstance(init, list):
            for key, value in init:
                self.add(key, value)
        elif isinstance(init, dict):
            self.data_dict = dict([(k, [v]) for k, v in dict.iteritems()])
            self.data_list = dict.items()
        else:
            raise TypeError('Invalid argument type for init argument.')


    def remove_any(self, key):
        if not self.data_dict.has_key(key):
            return
        old_values = self.data_dict.get(key)
        del self.data_dict[key]
        for value in old_values:
            self.data_list.remove((key, value))


    def add(self, key, value):
        """
        Adds the given key/value pair. Duplicate keys are allowed.

        @type  key: string
        @param key: The name of the attribute.
        @type  value: string
        @param value: The name of the attribute.
        """
        if not self.allow_duplicates:
            return self.set(key, value)
        self.data_list.append((key, value))
        if self.data_dict.has_key(key):
            self.data_dict[key].append(value)
        else:
            self.data_dict[key] = [value]


    def set(self, key, value):
        self.remove_any(key)
        self.data_dict[key] = [value]
        self.data_list.append((key, value))


    def get(self, key, default = None):
        return self.data_dict.get(key, default)


    def get_first(self, key, default):
        if not self.data_dict.has_key(key):
            return default
        for k, v in self.data_list:
            if k == key:
                return value
        assert False  # Not reached
