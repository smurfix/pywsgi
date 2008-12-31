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
import os, os.path, sha, time
from ConfigParser import RawConfigParser
from Table        import Table

class Session(object):
    def __init__(self, request, lifetime = 60 * 60):
        self.request     = request
        self.session_dir = request.get_session_directory()
        self.sid         = None
        self.rcparser    = RawConfigParser()
        self.lifetime    = lifetime
        if self.session_dir is None:
            raise Exception('Please call set_session_directory() first.')
        if not os.path.isdir(self.session_dir):
            raise Exception('No such directory: %s' % self.session_dir)
        self.start()


    def _clear_data(self, init = None):
        self.thedata = Table(init,
                             allow_duplicates = False,
                             callback         = self._on_data_changed)


    def _on_data_changed(self):
        self._save_session()


    def _get_session_filename(self):
        filename = ''
        for n in range(0, len(self.sid), 2):
            filename = os.path.join(filename, self.sid[n:n+2])
        return os.path.join(self.session_dir, filename + '.session')


    def _save_session(self):
        # Create a directory for the session.
        filename = self._get_session_filename()
        dirname  = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Save the session.
        try:
            self.rcparser.add_section('session')
        except:
            pass # Duplicate section.
        for key, value in self.thedata:
            self.rcparser.set('session', key, value)
        self.rcparser.write(open(filename, 'w'))


    def _load_session(self):
        """
        Returns True on success, False otherwise.
        """
        filename = self._get_session_filename()
        if not os.path.exists(filename):
            return False
        if os.path.getmtime(filename) < time.time() - self.lifetime:
            return False
        try:
            self.rcparser.read(filename)
        except:
            return False
        data = {}
        for option in self.rcparser.options('session'):
            data[option] = self.rcparser.get('session', option)
        self._clear_data(data)
        return True


    def _delete_session(self):
        filename = self._get_session_filename()
        if not os.path.exists(filename):
            return
        os.remove(filename)


    def _create_session(self):
        import sha, time
        self.sid = sha.new(str(time.time())).hexdigest()
        self.request.set_cookie('sid', self.sid, 0)
        self._save_session()


    def get_id(self):
        return self.sid


    def start(self):
        """
        May raise an exception on failure.
        """
        if self.sid is not None:
            raise Exception('Session already started.')
        self.sid = self.request.cookies().get_first('sid')
        if self.sid is None:
            return self._create_session()
        if not self._load_session():
            self.destroy()
            return self._create_session()


    def destroy(self):
        self._delete_session()
        self._clear_data()
        self.sid      = None
        self.rcparser = RawConfigParser()
        self.request.set_cookie('sid', '', 0)
        self.request._session_destroyed_notify()


    def data(self):
        """
        Returns the data that is associated with the session.

        @rtype:  Table
        @return: The session data.
        """
        return self.thedata