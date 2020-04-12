#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of todotxt-indicator
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
from config import _


class ListBoxRowStringType(Gtk.ListBoxRow):

    """Docstring for ListBoxRowStringType. """

    def __init__(self, text='', atype='string'):
        """TODO: to be defined. """
        Gtk.ListBoxRow.__init__(self)
        grid = Gtk.Grid.new()
        self.add(grid)
        self.name = Gtk.Label.new(text)
        self.name.set_halign(Gtk.Align.CENTER)
        self.name.set_width_chars(20)
        self.name.set_margin_top(5)
        self.name.set_margin_bottom(5)
        grid.attach(self.name, 0, 0, 1, 1)
        self.type = Gtk.Label.new(atype)
        self.type.set_halign(Gtk.Align.CENTER)
        self.type.set_width_chars(20)
        self.type.set_margin_top(5)
        self.type.set_margin_bottom(5)
        grid.attach(self.type, 1, 0, 1, 1)

    def get_name(self):
        return self.name.get_text()

    def set_name(self, text):
        self.name.set_text(text)

    def get_type(self):
        return self.type.get_text()

    def set_type(self, atype):
        self.type.set_text(atype)

        
class ListBoxStringType(Gtk.ListBox):

    """Docstring for ListBoxStringTyoe. """

    def __init__(self, items=[]):
        """TODO: to be defined. """
        Gtk.ListBox.__init__(self)
        if len(items) > 0:
            self.add_all(items)
    
    def add_all(self, items):
        for item in items:
            self.add_item(item)
            
    def add_item(self, new_item):
        for item in self.get_children():
            if item.get_name() == new_item['name']:
                return
        newListBoxRowStringType = ListBoxRowStringType(new_item['name'], new_item['type'])
        newListBoxRowStringType.show_all()
        self.add(newListBoxRowStringType)

    def remove_item(self, text):
        for index, item in enumerate(self.get_children()):
            if self.get_children()[index].get_name() == text:
                self.remove(self.get_children()[index])
                return

    def clear(self):
        for index in range(len(self.get_children()) -1, -1):
            self.remove(self.get_children()[index])

    def get_items(self):
        items = []
        for child in self.get_children():
            item = {}
            items.append({'name': child.get_name(), 'type': child.get_type()})
        return items
