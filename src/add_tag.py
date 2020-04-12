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


class AddTagDialog(BaseDialog):

    """Docstring for AddTagDialog. """

    def __init__(self):
        """TODO: to be defined. """
        BaseDialog.__init__(self, _('Add Tag'), None, ok_button=True,
                            cancel_button=True)
        select_value_in_combo(self.type, 'string')
       
    def init_ui(self):
        BaseDialog.init_ui(self)

        label = Gtk.Label.new(_('Tag name:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 0, 1, 1)

        self.text = Gtk.Entry.new()
        self.grid.attach(self.text, 1, 0, 1, 1)

        label = Gtk.Label.new(_('Type:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 1, 1, 1)

        type_store = Gtk.ListStore(str, str)
        type_store.append(['Date', 'date'])
        type_store.append(['Number', 'number'])
        type_store.append(['String', 'string'])

        self.type = Gtk.ComboBox.new()
        self.type.set_model(type_store)
        cell1 = Gtk.CellRendererText()
        self.type.pack_start(cell1, True)
        self.type.add_attribute(cell1, 'text', 0)
        self.grid.attach(self.type, 1, 1, 1, 1)

    def get_type(self):
        return get_selected_value_in_combo(self.type)

    def get_name(self):
        """TODO: Docstring for get_name.
        :returns: TODO

        """
        return self.text.get_text()

if __name__ == '__main__':
    addTagDialog = AddTagDialog()
    response = addTagDialog.run()
    if response == Gtk.ResponseType.ACCEPT:
        addTagDialog.get_task()
    addTagDialog.destroy()
        
