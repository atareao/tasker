#!/usr/bin/env python
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
# copies of the Software, nd to permit persons to whom the Software is
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
from gi.repository import GObject, Gtk

try:
    gi.require_version("Gtk", "3.0")
except Exception as e:
    print(e)
    exit(-1)


class ListBoxRowPlugins(Gtk.ListBoxRow):
    """Docstring for ListBoxRowCheck. """

    __gsignals__ = {
        "toggled": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, plugin):
        """TODO: to be defined. """
        Gtk.ListBoxRow.__init__(self)
        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.add(self.box)

        self.plugin = plugin
        self.visible = True

        self.switch = Gtk.CheckButton.new()
        self.switch.set_active(self.plugin["installed"])
        self.box.add(self.switch)
        self.switch.connect("toggled", self.on_toggled)

        text = self.plugin["name"]
        self.label = Gtk.Label.new("")
        self.label.set_use_markup(True)
        self.label.set_markup(text)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_margin_bottom(5)
        self.box.add(self.label)

    def on_toggled(self, widget):
        self.emit("toggled")

    def get_plugin(self):
        self.plugin["installed"] = self.switch.get_active()
        return self.plugin


class ListBoxPlugins(Gtk.ScrolledWindow):
    """Docstring for ListBoxCheck. """

    __gsignals__ = {
        "toggled": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, items=[]):
        """TODO: to be defined. """
        Gtk.ScrolledWindow.__init__(self)
        self.listBox = Gtk.ListBox.new()
        self.add(self.listBox)
        if len(items) > 0:
            self.add_all(items)

    def add_all(self, items):
        for item in items:
            self.add_item(item)

    def add_item(self, plugin):
        newListBoxRowPlugin = ListBoxRowPlugins(plugin)
        newListBoxRowPlugin.show_all()
        newListBoxRowPlugin.connect("toggled", self.on_toggled)
        self.listBox.add(newListBoxRowPlugin)

    def on_toggled(self, widget):
        self.emit("toggled")

    def get_items(self):
        items = []
        for child in self.listBox.get_children():
            items.append(child.get_plugin())
        return items

    def unselect(self):
        return self.listBox.select_row(None)

    def get_selected(self):
        return self.listBox.get_selected_row()

    def set_selected(self, plugin):
        selected_row = self.listBox.get_selected_row()
        if selected_row:
            selected_row.set_plugin(plugin)
