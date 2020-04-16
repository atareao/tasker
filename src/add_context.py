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
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from config import _
from basedialog import BaseDialog

class AddContextDialog(BaseDialog):

    """Docstring for AddContextDialog. """

    def __init__(self):
        """TODO: to be defined. """
        BaseDialog.__init__(self, _('Add Context'), None, ok_button=True,
                            cancel_button=True)
       
    def init_ui(self):
        BaseDialog.init_ui(self)

        label = Gtk.Label.new(_('Context name:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 0, 1, 1)

        self.text = Gtk.Entry.new()
        self.grid.attach(self.text, 1, 0, 1, 1)

    def get_name(self):
        """TODO: Docstring for get_name.
        :returns: TODO

        """
        return self.text.get_text()


if __name__ == '__main__':
    addContextDialog = AddContextDialog()
    response = addContextDialog.run()
    if response == Gtk.ResponseType.ACCEPT:
        addContextDialog.get_task()
    addContextDialog.destroy()
        
