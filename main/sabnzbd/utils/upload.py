#!/usr/bin/python -OO
# Copyright 2009 The SABnzbd-Team <team@sabnzbd.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
sabnzbd.utils.upload - File assosiation functions for adding nzb files to sabnzbd
"""

import urllib2
import urllib
import logging
import os
import sabnzbd.cfg as cfg
from sabnzbd.misc import get_ext, get_filename
from sabnzbd.dirscanner import ProcessArchiveFile, ProcessSingleFile

def upload_file(url, fp):
    """ Function for uploading nzbs to a running sabnzbd instance """
    try:
        fp = urllib.quote_plus(fp)
        pp = cfg.DIRSCAN_PP()
        script = cfg.DIRSCAN_SCRIPT()
        priority = cfg.DIRSCAN_PRIORITY()
        url = '%sapi?mode=addlocalfile&name=%s&pp=%s&script=%s&priority=%s' % (url, fp, pp, script, priority)
        username = cfg.USERNAME()
        password = cfg.PASSWORD()
        apikey = cfg.API_KEY()
        if username and password:
            url = '%s&ma_username=%s&ma_password=%s' % (url, username, password)
        if apikey:
            url = '%s&apikey=%s' % (url, apikey)
        u = urllib2.urlopen(url)
    except:
        logging.error("Failed to upload file: %s", fp)
        logging.debug("Traceback: ", exc_info = True)


def add_local(f):
    """ Function for easily adding nzb/zip/rar/nzb.gz to sabnzbd """
    if os.path.exists(f):
        fn = get_filename(f)
        if fn:
            pp = cfg.DIRSCAN_PP()
            script = cfg.DIRSCAN_SCRIPT()
            priority = cfg.DIRSCAN_PRIORITY()
            if get_ext(fn) in ('.zip','.rar', '.gz'):
                ProcessArchiveFile(fn, f, pp=pp, script=script, priority=priority, keep=True)
            elif get_ext(fn) in ('.nzb'):
                ProcessSingleFile(fn, f, pp=pp, script=script, priority=priority, keep=True)
        else:
            logging.error("Filename not found: %s", f)
    else:
        logging.error("File not found: %s", f)