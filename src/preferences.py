#!/usr/bin/env python3
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
    gi.require_version('Gio', '2.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gio
from pathlib import Path
import os
import config
import shutil
from config import _
from configurator import Configuration
from basedialog import BaseDialog


def select_value_in_combo(combo, value):
    model = combo.get_model()
    for i, item in enumerate(model):
        if value == item[1]:
            combo.set_active(i)
            return
    combo.set_active(0)


def get_selected_value_in_combo(combo):
    model = combo.get_model()
    return model.get_value(combo.get_active_iter(), 1)


class Preferences(BaseDialog):
    def __init__(self):
        BaseDialog.__init__(self, _('Preferences'), None, ok_button=True,
                            cancel_button=True)
        self.load()

    def init_ui(self):
        BaseDialog.init_ui(self)
        label = Gtk.Label.new(_('Theme light:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 0, 1, 1)
        
        self.theme_light = Gtk.Switch.new()
        self.theme_light.set_property('halign', Gtk.Align.CENTER)
        self.grid.attach(self.theme_light, 1, 0, 1, 1)
        
        label = Gtk.Label.new(_('Autostart'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 1, 1, 1)

        self.autostart = Gtk.Switch.new()
        self.autostart.set_property('halign', Gtk.Align.CENTER)
        self.grid.attach(self.autostart, 1, 1, 1, 1)

        self.grid.attach(Gtk.Separator(), 0, 2, 2, 1)

        label = Gtk.Label.new(_('Number of todos:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 3, 1, 1)

        self.todos = Gtk.SpinButton.new_with_range(1, 20, 1)
        self.grid.attach(self.todos, 1, 3, 1, 1)
       
        label = Gtk.Label.new(_('Number of dones:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 4, 1, 1)

        self.dones = Gtk.SpinButton.new_with_range(1, 10, 1)
        self.grid.attach(self.dones, 1, 4, 1, 1)

        self.grid.attach(Gtk.Separator(), 0, 5, 2, 1)

        label = Gtk.Label.new(_('Todo file:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 6, 1, 1)

        todofilter = Gtk.FileFilter.new()
        todofilter.add_pattern('*.txt')
        todofilter.add_mime_type('text/plain')

        self.todo_file = Gtk.FileChooserButton.new(_('Todo file'), Gtk.FileChooserAction.OPEN)
        self.todo_file.add_filter(todofilter)
        self.grid.attach(self.todo_file, 1, 6, 1, 1)
        
        label = Gtk.Label.new(_('Done file:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 7, 1, 1)

        self.done_file = Gtk.FileChooserButton.new(_('Done file'), Gtk.FileChooserAction.OPEN)
        self.done_file.add_filter(todofilter)
        self.grid.attach(self.done_file, 1, 7, 1, 1)


    def load(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        self.theme_light.set_active(preferences.get('theme-light'))
        autostart_file = 'todotxt-indicator-autostart.desktop'
        if os.path.exists(os.path.join(
                os.getenv('HOME'), '.config/autostart', autostart_file)):
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)
        self.todos.set_value(preferences['todos'])
        self.dones.set_value(preferences['dones'])
        todo_file = Path(os.path.expanduser(preferences['todo-file']))
        if not todo_file.exists():
            if not todo_file.parent.exists():
                os.makedirs(todo_file.parent)
            todo_file.touch()
        self.todo_file.set_file(Gio.File.new_for_path(todo_file.as_posix()))
        done_file = Path(os.path.expanduser(preferences['done-file']))
        if not done_file.exists():
            if not done_file.parent.exists():
                on.makedirs(todo_file.parent)
            done_file.touch()
        self.done_file.set_file(Gio.File.new_for_path(done_file.as_posix()))


    def save(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        preferences['theme-light'] = self.theme_light.get_active()
        preferences['todos'] = int(self.todos.get_value())
        preferences['dones'] = int(self.dones.get_value())
        preferences['todo-file'] = self.todo_file.get_file().get_path()
        preferences['done-file'] = self.done_file.get_file().get_path()
        configuration.set('preferences', preferences)
        configuration.save()
        autostart_file = 'todotxt-indicator-autostart.desktop'
        autostart_file = os.path.join(
                os.getenv('HOME'), '.config/autostart', autostart_file)
        if self.autostart.get_active():
            if not os.path.exists(os.path.dirname(autostart_file)):
                os.makedirs(os.path.dirname(autostart_file))
            shutil.copyfile(config.AUTOSTART, autostart_file)
        else:
            if os.path.exists(autostart_file):
                os.remove(autostart_file)



if __name__ == '__main__':
    preferences = Preferences()
    response = preferences.run()
    if response == Gtk.ResponseType.ACCEPT:
        preferences.save()
    preferences.destroy()
