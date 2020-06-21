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

import os
from pathlib import Path

import config
import gi
from basedialog import BaseDialog
from config import _
from configurator import Configuration
from todotxtio import todotxtio

try:
    gi.require_version("Gtk", "3.0")
    gi.require_version("WebKit2", "4.0")
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk, WebKit2  # isort:skip


class BaseGraph(BaseDialog):
    """
    Class that allows the visualization of graphs with highcharts.js


    To implement your own graphs, simply override the get_data method or use get_keys and get_values
    that are related to each other
    """

    def __init__(self, title="", subtitle=""):
        self.title = _(title)
        self.configuration = Configuration()
        preferences = self.configuration.get("preferences")
        todo_file = Path(os.path.expanduser(preferences["todo-file"]))
        self.todo_file = todo_file.as_posix()
        self.subtitle = _(subtitle)
        BaseDialog.__init__(
            self, title, None, ok_button=False, cancel_button=False
        )

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
        )
        self.grid.attach(self.scrolledwindow1, 0, 0, 1, 1)

        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(1300, 600)
        self.viewer.load_uri("file://" + config.HTML_GRAPH)
        self.viewer.connect("load-changed", self.load_changed)
        self.set_focus(self.viewer)

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.send_data()

    def send_data(self):
        message = 'draw_graph("{}", "{}", {});'.format(
            self.title, self.subtitle, self.get_data()
        )

        self.viewer.run_javascript(message, None, None, None)

    def get_data(self,):
        plaindata = self.get_plaindata()
        keys = self.get_keys(plaindata)
        values = self.get_values(keys, plaindata)
        return {"keys": keys, "values": values}

    def get_plaindata(self,):
        return todotxtio.from_file(self.todo_file)

    def get_keys(self, plaindata):
        return super().get_keys(plaindata)

    def get_values(self, keys, plaindata):
        return super().get_values(keys, plaindata)


if __name__ == "__main__":
    graph = BaseGraph(_("Testing graph"))
    graph.run()
