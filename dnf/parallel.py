# Copyright (C) 2017 Benjamin Chaney
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Written by Benjamin Chaney

import sys
import threading
from __future__ import print_function
try:
    import queue
except ImportError:
    #python 2
    import Queue as queue


class DownloadTask (Thread):
    base = None
    pkgs = None
    output_queue = None

    def __init__(self, base, pkgs, output_queue):
        self.base = base
        self.pkgs = pkgs
        self.output_queue = output_queue

    def run(self):
        for pkg in pkgs:
            remote_pkg = base.select_remote_pkgs([pkg])
            if remote_pkg:
                try:
                    base.download_packages(remote_pkg, base.output.progress,
                                           base.output.download_callback_total_cb)
                except dnf.exceptions.DownloadError as e:
                    specific = dnf.cli.format.indent_block(ucd(e))
                    errstr = _('Error downloading package: ') + '%s\n%s' % pkg, specific
                    # setting the new line to prevent next chars being eaten up
                    # by carriage returns
                    print()
                    print(errstr, file=sys.stderr)
            base.gpgsigcheck([pkg])
            output_queue.put(pkg)

