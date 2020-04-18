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
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import GObject

class ListBoxRowCheck(Gtk.ListBoxRow):
    """Docstring for ListBoxRowCheck. """
    __gsignals__ = {
        'toggled': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, text):
        """TODO: to be defined. """
        Gtk.ListBoxRow.__init__(self)
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.add(box)

        self.switch = Gtk.CheckButton.new()
        self.switch.connect('toggled', self.on_toggled)
        box.add(self.switch)

        self.label = Gtk.Label.new(text)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_margin_bottom(5)
        box.add(self.label)

    def on_toggled(self, widget):
        self.emit('toggled')

    def get_name(self):
        return self.label.get_text()

    def set_name(self, text):
        self.label.set_text(text)

    def set_active(self, active):
        self.switch.set_active(active)

    def get_active(self):
        return self.switch.get_active()


class ListBoxCheck(Gtk.ScrolledWindow):
    """Docstring for ListBoxCheck. """
    __gsignals__ = {
        'toggled': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }


    def __init__(self, items=[]):
        """TODO: to be defined. """
        Gtk.ScrolledWindow.__init__(self)
        self.listBox = Gtk.ListBox.new()
        self.listBox.set_sort_func(self.sort_list)
        self.add(self.listBox)
        if len(items) > 0:
            self.add_all(items)

    def sort_list(self, row1, row2):
        """TODO: Docstring for sort_list.

        :row1: TODO
        :row2: TODO
        :returns: TODO

        """
        return row1.get_name() > row2.get_name()

    def add_all(self, items):
        for item in items:
            self.add_item(item)

    def add_item(self, text):
        for item in self.get_children():
            if item.get_name() == text:
                return
        newListBoxRowCheck = ListBoxRowCheck(text)
        newListBoxRowCheck.show_all()
        newListBoxRowCheck.connect('toggled', self.on_toggled)
        self.listBox.add(newListBoxRowCheck)

    def on_toggled(self, widget):
        self.emit('toggled')

    def remove_item(self, text):
        for index, item in enumerate(self.listBox.get_children()):
            if self.listBox.get_children()[index].get_name() == text:
                self.remove(self.listBox.get_children()[index])
                return

    def clear(self):
        for index in range(len(self.listBox.get_children()) -1, -1):
            self.remove(self.listBox.get_children()[index])

    def get_items(self):
        items = []
        for child in self.listBox.get_children():
            items.append(child.get_name())
        return items
                

    def get_active_items(self):
        items = []
        for child in self.listBox.get_children():
            if child.get_active():
                items.append(child.get_name())
        return items

    def set_active_items(self, items):
        """TODO: Docstring for set_active_items.

        :items: TODO
        :returns: TODO

        """
        for child in self.listBox.get_children():
            child.set_active(child.get_name() in items)
