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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('WebKit2', '4.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import WebKit2
import config
from basedialog import BaseDialog
from configurator import Configuration
import todotxtio.todotxtio as todotxtio
import os
from pathlib import Path

class Graph(BaseDialog):
    def __init__(self, title='', by_project=True):
        self.title = title
        self.configuration = Configuration()
        preferences = self.configuration.get('preferences')
        todo_file = Path(os.path.expanduser(preferences['todo-file']))
        self.todo_file = todo_file.as_posix()
        self.by_project = by_project
        if by_project:
            self.subtitle = _('By project')
        else:
            self.subtitle = _('By context')
        BaseDialog.__init__(self, title, None, ok_button=False,
                            cancel_button=False)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(self.scrolledwindow1, 0, 0, 1, 1)

        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(1300, 600)
        self.viewer.load_uri('file://' + config.HTML_GRAPH)
        self.viewer.connect('load-changed', self.load_changed)
        self.set_focus(self.viewer)

    def update_projects(self):
        list_of_todos = todotxtio.from_file(self.todo_file)
        projects = []
        empty = False
        for todo in list_of_todos:
            if todo.projects:
                for project in todo.projects:
                    if project not in projects:
                        projects.append(project)
            else:
                empty = True
        if empty:
            projects.append(_('None'))
        projects.sort()
        values = []
        for todo in list_of_todos:
            data = []
            for project in projects:
                if project in todo.projects:
                    data.append(float(todo.tags.get('total_time', '0'))/3600.0)
                elif not todo.projects and project == _('None'):
                    data.append(float(todo.tags.get('total_time', '0'))/3600.0)
                else:
                    data.append(0)
            values.append({'name': todo.text, 'data': data})
        measure = {'dates': projects, 'values': values}
        self.web_send('draw_graph("{}", "{}", {});'.format(
            self.title, self.subtitle,  measure))

    def update_contexts(self):
        list_of_todos = todotxtio.from_file(self.todo_file)
        contexts = []
        empty = False
        for todo in list_of_todos:
            if todo.contexts:
                for context in todo.contexts:
                    if context not in contexts:
                        contexts.append(context)
            else:
                empty = True
        if empty:
            contexts.append(_('None'))
        contexts.sort()
        values = []
        for todo in list_of_todos:
            data = []
            for context in contexts:
                if context in todo.contexts:
                    data.append(float(todo.tags.get('total_time', '0'))/3600.0)
                elif not todo.contexts and context == _('None'):
                    data.append(float(todo.tags.get('total_time', '0'))/3600.0)
                else:
                    data.append(0)
            values.append({'name': todo.text, 'data': data})
        measure = {'dates': contexts, 'values': values}
        self.web_send('draw_graph("{}", "{}", {});'.format(
            self.title, self.subtitle,  measure))

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            if self.by_project:
                self.update_projects()
            else:
                self.update_contexts()

    def web_send(self, msg):
        self.viewer.run_javascript(msg, None, None, None)


if __name__ == '__main__':
    title = 'Timetracking tasker'
    measure = {
        'dates': [
            '08-05-2020',
            '09-05-2020',
            '10-05-2020',
            '11-05-2020',
            '12-05-2020',
            '13-05-2020',
            '14-05-2020',
            '15-05-2020',
            '16-05-2020',
            '17-05-2020',
            '18-05-2020',
            '19-05-2020',
            '20-05-2020',
            '21-05-2020',
        ],
        'values': [
            {
                'name': 'Task 1:Proj 1',
                'data': [3, 3, 0, 7, 5, 2, 3, 4, 1, 2, 3, 4, 0, 0]
            }, {
                'name': 'Task 2:Proj 1',
                'data': [4, 3, 4, 0, 0, 2, 3, 4, 1, 2, 3, 4, 0, 0]
            }, {
                'name': 'Task 3:Proj 2',
                'data': [1, 2, 4, 0, 3, 2, 3, 4, 1, 2, 3, 4, 0, 0]
            },
        ]
    }
    graph = Graph(title)
    graph.run()
