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
from gi.repository import GObject

class ListBoxRowTodo(Gtk.ListBoxRow):
    """Docstring for ListBoxRowCheck. """
    __gsignals__ = {
        'toggled': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, todo):
        """TODO: to be defined. """
        Gtk.ListBoxRow.__init__(self)
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.add(box)

        self.todo = todo

        self.switch = Gtk.CheckButton.new()
        self.switch.set_active(self.todo.completed)
        box.add(self.switch)
        self.switch.connect('toggled', self.on_toggled)

        self.label = Gtk.Label.new(self.todo.text)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_margin_bottom(5)
        box.add(self.label)

    def get_todo(self):
        self.todo.completed = self.switch.get_active()
        return self.todo

    def set_todo(self, todo):
        self.todo = todo
        self.label.set_text(todo.text)
        self.label.show_all()
        self.switch.set_active(todo.completed)

    def set_completed(self, completed):
        self.todo.completed = completed
        self.switch.set_active(completed)

    def get_completed(self):
        return self.switch.get_active()

    def on_toggled(self, widget, status):
        self.emit('toggled')


class ListBoxTodo(Gtk.ScrolledWindow):
    """Docstring for ListBoxCheck. """
    __gsignals__ = {
        'toggled': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
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
            
    def add_item(self, todo):
        for item in self.listBox.get_children():
            if item.get_todo().text == todo.text and \
                    item.get_todo().projects == todo.projects and \
                    item.get_todo().contexts == todo.contexts:
                return
        newListBoxRowTodo = ListBoxRowTodo(todo)
        newListBoxRowTodo.show_all()
        newListBoxRowTodo.connect('toggled', self.on_toggled)
        self.listBox.add(newListBoxRowTodo)

    def on_toggled(self, widget):
        self.emit('toggled')

    def remove_item(self, todo):
        for index, item in enumerate(self.listBox.get_children()):
            if item.get_todo().text == todo.text and \
                    item.get_todo().projects == todo.projects and \
                    item.get_todo().contexts == todo.contexts:
                self.listBox.remove(self.listBox.get_children()[index])
                return

    def clear(self):
        for index in range(len(self.listBox.get_children()) -1, -1, -1):
            self.listBox.remove(self.listBox.get_children()[index])

    def get_items(self):
        items = []
        for child in self.listBox.get_children():
            items.append(child.get_todo())
        return items

    def get_completed_items(self):
        items = []
        for child in self.listBox.get_children():
            if child.get_completed():
                items.append(child.get_todo())
        return items

    def get_selected(self):
        return self.listBox.get_selected_row()

    def set_selected(self, todo):
        selected_row = self.listBox.get_selected_row()
        if selected_row:
            selected_row.set_todo(todo)
