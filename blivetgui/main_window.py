# -*- coding: utf-8 -*-
# main_window.py
# blivet-gui Main Window
#
# Copyright (C) 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Vojtech Trefny <vtrefny@redhat.com>
#
#------------------------------------------------------------------------------#

from __future__ import print_function

import os, signal

from gi.repository import Gtk

import gettext

from list_devices import ListDevices

from udisks_loop import udisks_thread

#------------------------------------------------------------------------------#

_ = lambda x: gettext.ldgettext("blivet-gui", x)

#------------------------------------------------------------------------------#

def locate_ui_file(filename):

    path = [os.path.split(os.path.abspath(__file__))[0] + '/../data/ui/',
        '/usr/share/blivet-gui/ui/']

    for folder in path:
        fn = folder + filename
        if os.access(fn, os.R_OK):
            return fn

    raise RuntimeError("Unable to find glade file %s" % file)

def main_window(kickstart=False):
    """ Create main window from Glade UI file
    """

    builder = Gtk.Builder()
    builder.add_from_file(locate_ui_file('blivet-gui.ui'))

    MainWindow = builder.get_object("MainWindow")

    ListDevices(MainWindow, builder, kickstart)

    # u = udisks_thread()
    # u.start()

    return MainWindow

def embeded_window(kickstart=False):
    """ Create Gtk.Plug widget
    """

    window_id = 0
    plug = Gtk.Plug(window_id)

    print(str(plug.get_id()) + "\n")

    builder = Gtk.Builder()
    builder.add_from_file(locate_ui_file('blivet-gui.ui'))

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    vbox = builder.get_object("vbox")
    vbox.reparent(plug)

    ListDevices(plug, builder, kickstart)

    return plug
