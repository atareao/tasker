#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of tasker
#
# Copyright (c) 2020 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import locale
import gettext

PARAMS = {'stats': {},
          'preferences': {'theme-light': True,
                          'start-actived': True,
                          'todos': 10,
                          'todo-file': '~/.config/tasker/todo.txt',
                          'hide-completed': False,
                          'filter-projects': False,
                          'projects': [],
                          'keybindings': [
                               {
                                   'keybind': '<Control><Super>t',
                                   'name': 'new_task'
                               },
                               {
                                   'keybind': '<Control><Super>a',
                                   'name': 'show_tasks'
                               }
                           ],
                          'contexts': [],
                          'tags': [
                              {
                                  'name': 'due',
                                  'type': 'date'
                              },
                              {
                                  'name': 'started_at',
                                  'type': 'string'
                              },
                              {
                                  'name': 'total_time',
                                  'type': 'string'
                              },
                          ]
                          }
          }

CONFIG_DIR = os.path.join(os.path.expanduser('~'),
                          '.config/tasker')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'tasker.conf')
DATA_FILE = os.path.join(CONFIG_DIR, 'tasker.data')


def is_package():
    return __file__.find('src') < 0


APP = 'tasker'
APPNAME = 'TodoTxt Indicator'

# check if running from source
if is_package():
    ROOTDIR = '/opt/extras.ubuntu.com/tasker/share'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    ICONDIR = os.path.join(ROOTDIR, 'icons')
    HTML_GRAPH = os.path.join(APPDIR, 'graph', 'graph.html')
    AUTOSTARTDIR = os.path.join(ROOTDIR, 'autostart')
else:
    ROOTDIR = os.path.abspath(os.path.dirname(__file__))
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons/'))
    HTML_GRAPH = os.path.join(ROOTDIR, 'graph', 'graph.html')
    AUTOSTARTDIR = os.path.normpath(
        os.path.join(ROOTDIR, '../data/autostart/'))
AUTOSTART = os.path.join(AUTOSTARTDIR, 'tasker-autostart.desktop')
ICON = os.path.join(ICONDIR, 'tasker.svg')
ICON_ACTIVED_LIGHT = os.path.join(ICONDIR, 'tasker-active-light.svg')
ICON_PAUSED_LIGHT = os.path.join(ICONDIR, 'tasker-paused-light.svg')
ICON_ACTIVED_DARK = os.path.join(ICONDIR, 'tasker-active-dark.svg')
ICON_PAUSED_DARK = os.path.join(ICONDIR, 'tasker-paused-dark.svg')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    if sys.version_info[0] == 3:
        _ = language.gettext
    else:
        _ = language.ugettext
except Exception as e:
    print(e)
    _ = str
APPNAME = _(APPNAME)
