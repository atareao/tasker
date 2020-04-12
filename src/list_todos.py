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
import os
from pathlib import Path
import todotxtio.todotxtio as todotxtio
from basedialog import BaseDialog
from list_box_check import ListBoxCheck
from list_box_todo import ListBoxTodo
from add_todo import AddTodoDialog
from config import _
from configurator import Configuration


class ListTodos(BaseDialog):
    """docstring for ListTodos"""
    def __init__(self):
        BaseDialog.__init__(self, _('List of todos'), None, ok_button=True,
                            cancel_button=True)
        self.load()

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.todos = ListBoxTodo()
        self.todos.set_size_request(300, 500)
        self.grid.attach(self.todos, 0, 0, 1, 1)

        expander = Gtk.Expander.new(_('Filter by project(s) and context(s)'))
        notebook = Gtk.Notebook.new()
        expander.add(notebook)
        # self.grid.attach(expander, 0, 1, 1, 1)

        page01 = Gtk.Grid.new()
        page01.set_row_spacing(10)
        page01.set_margin_bottom(10)
        page01.set_margin_start(10)
        page01.set_margin_end(10)
        page01.set_margin_top(10)
        notebook.append_page(page01, Gtk.Label.new(_('Select project(s)')))

        self.projects = ListBoxCheck()
        self.projects.connect('toggled', self.on_toggled)
        self.projects.set_size_request(300, 80)
        page01.attach(self.projects, 0, 0, 1, 1)

        page02 = Gtk.Grid.new()
        page02.set_row_spacing(10)
        page02.set_margin_bottom(10)
        page02.set_margin_start(10)
        page02.set_margin_end(10)
        page02.set_margin_top(10)
        notebook.append_page(page02, Gtk.Label.new(_('Select context(s)')))

        self.contexts = ListBoxCheck()
        self.contexts.connect('toggled', self.on_toggled)
        self.contexts.set_size_request(300, 80)
        page02.attach(self.contexts, 0, 0, 1, 1)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.grid.attach(box, 1, 0, 1, 2)

        button_add = Gtk.Button.new_with_label(_('Add'))
        button_add.connect('clicked', self.on_button_add_clicked)
        box.add(button_add)

        button_edit = Gtk.Button.new_with_label(_('Edit'))
        button_edit.connect('clicked', self.on_button_edit_clicked)
        box.add(button_edit)

        button_remove = Gtk.Button.new_with_label(_('Remove'))
        button_remove.connect('clicked', self.on_button_remove_clicked)
        box.add(button_remove)

        button_clear = Gtk.Button.new_with_label(_('Clear'))
        button_clear.connect('clicked', self.on_button_clear_clicked)
        box.add(button_clear)

    def on_toggled(self, widget):
        list_of_todos = self.todos.get_items()
        results = todotxtio.search(list_of_todos, contexts=self.contexts.get_items(), projects=self.projects.get_items())

    def on_button_clear_clicked(self, widget):
        self.todos.clear()

    def on_button_add_clicked(self, widget):
        addTodoDialog = AddTodoDialog()
        if addTodoDialog.run() == Gtk.ResponseType.ACCEPT:
            todo = addTodoDialog.get_task()
            self.todos.add_item(todo)
        addTodoDialog.destroy()

    def on_button_edit_clicked(self, widget):
        selected = self.todos.get_selected()
        if selected:
            todo = selected.get_todo()
            addTodoDialog = AddTodoDialog(todo)
            if addTodoDialog.run() == Gtk.ResponseType.ACCEPT:
                todo = addTodoDialog.get_task()
                self.todos.set_selected(todo)
            addTodoDialog.destroy()

    def on_button_remove_clicked(self, widget):
        selected = self.todos.get_selected()
        if selected:
            todo = selected.get_todo()
            self.todos.remove_item(todo)

    def load(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        projects = preferences['projects']
        self.projects.add_all(projects)
        self.projects.set_active_items(projects)
        contexts = preferences['contexts']
        self.contexts.add_all(contexts)
        self.contexts.set_active_items(contexts)

        todo_file = Path(os.path.expanduser(preferences['todo-file']))
        if not todo_file.exists():
            if not todo_file.parent.exists():
                os.makedirs(todo_file.parent)
            todo_file.touch()
        self.todo_file = todo_file.as_posix()
        self.load_todos()

    def load_todos(self):
        list_of_todos = todotxtio.from_file(self.todo_file)
        self.todos.add_all(list_of_todos)

    def save(self):
        todotxtio.to_file(self.todo_file, self.todos.get_items())

    def filter(self):
        active_projects = self.projects.get_active_items()
        active_contexts = self.contexts.get_active_items()
        print(active_projects, active_contexts)


if __name__ == '__main__':
    listTodos = ListTodos()
    response = listTodos.run()
    if response == Gtk.ResponseType.ACCEPT:
        listTodos.save()
    listTodos.destroy()
