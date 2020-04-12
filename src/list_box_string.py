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

class ListBoxRowString(Gtk.ListBoxRow):

    """Docstring for ListBoxRowString. """

    def __init__(self, text):
        """TODO: to be defined. """
        Gtk.ListBoxRow.__init__(self)
        label = Gtk.Label.new(text)
        label.set_halign(Gtk.Align.CENTER)
        label.set_width_chars(20)
        label.set_margin_top(5)
        label.set_margin_bottom(5)
        self.add(label)

    def get_name(self):
        return self.get_children()[0].get_text()

    def set_name(self, text):
        self.get_children()[0].set_text(text)

        
class ListBoxString(Gtk.ListBox):

    """Docstring for ListBoxString. """

    def __init__(self, items=[]):
        """TODO: to be defined. """
        Gtk.ListBox.__init__(self)
        if len(items) > 0:
            self.add_all(items)
    
    def add_all(self, items):
        for item in items:
            self.add_item(item)
            
    def add_item(self, text):
        for item in self.get_children():
            if item.get_name() == text:
                return
        newListBoxRowString = ListBoxRowString(text)
        newListBoxRowString.show_all()
        self.add(newListBoxRowString)

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
            items.append(child.get_name())
        return items
                

        
