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
import os, os.path, sha
from ConfigParser import RawConfigParser

class Session(object):
    def __init__(self, request, lifetime = 60 * 60):
        self.session_dir = request.get_session_directory()
        self.request     = kwargs['request']
        self.sid         = None
        self.data        = {}
        self.rcparser    = RawConfigParser()
        self.lifetime    = lifetime
        if self.session_directory is None:
            raise Exception('Please call set_session_directory() first.')
        if not os.path.isdir(self.session_directory):
            raise Exception('No such directory: %s' % self.session_dir)
        self.start()


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
            os.path.makedirs(dirname)

        # Save the session.
        self.rcparser.add_section('session')
        for key, value in self.data.iteritems():
            self.rcparser.set('session', key, value)
        self.rcparser.write(open(filename, 'w'))


    def _load_session(self):
        """
        Returns True on success, False otherwise.
        """
        filename = self._get_session_filename()
        if not os.path.exists(filename):
            return False
        if os.path.getmtime(filename) < time() - self.lifetime:
            return False
        try:
            self.rcparser.read(filename)
        except:
            return False
        for option in self.rcparser.options('session'):
            self.data[option] = self.rcparser.get('session', option)
        return True


    def _delete_session(self):
        filename = self._get_session_filename()
        if not os.path.exists(filename):
            return
        os.remove(self.filename)


    def _create_session(self):
        import sha, time
        self.sid = sha.new(str(time.time())).hexdigest()
        self._save_session()


    def get_id(self):
        return self.sid


    def start(self):
        """
        May raise an exception on failure.
        """
        if self.sid is not None:
            raise Exception('Session already started.')
        self.sid = self.request.get_cookie('sid')
        if self.sid is None:
            return self._create_session()
        if not self._load_session():
            self.destroy()
            return self._create_session()


    def destroy(self):
        self.sid      = None
        self.data     = {}
        self.rcparser = RawConfigParser()
        self._delete_session()
        self.request.set_cookie('sid', '', 0)
