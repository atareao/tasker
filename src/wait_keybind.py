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
from basedialog import BaseDialog
from config import _
from gi.repository import Gdk, Gtk

try:
    gi.require_version("Gtk", "3.0")
except ValueError as e:
    print(e)
    exit(1)


class WaitKeybind(BaseDialog):
    def __init__(self):
        BaseDialog.__init__(
            self,
            _("Waiting for keybind"),
            None,
            ok_button=True,
            cancel_button=True,
        )

    def init_ui(self):
        BaseDialog.init_ui(self)
        label_waiting = Gtk.Label.new(_("Capturing new keybind"))
        label_waiting.set_property("halign", Gtk.Align.START)
        label_waiting.set_property("can_focus", False)
        self.grid.attach(label_waiting, 0, 0, 1, 1)

        self.key_pressed = []
        self.key_unpressed = []
        self.shortcut_hits = 0
        self.label = Gtk.Label(label="")
        self.update_label_text()
        self.grid.attach(self.label, 0, 1, 1, 1)

        self.connect("key-press-event", self.on_key_press_event)
        self.connect("key-release-event", self.on_key_release_event)

    def on_key_press_event(self, widget, event):
        keyval = Gdk.keyval_to_lower(event.keyval)
        if keyval not in self.key_pressed:
            self.key_pressed.append(keyval)

    def on_key_release_event(self, widget, event):
        keyval = Gdk.keyval_to_lower(event.keyval)
        try:
            self.key_pressed.remove(keyval)
        except Exception as e:
            print(e)
        self.key_unpressed.append(keyval)

        if not len(self.key_pressed) and len(self.key_unpressed):
            response_arr = [
                Gdk.keyval_name(keyval).split("_")[0]
                if len(Gdk.keyval_name(keyval).split("_")[0]) <= 2
                else "<" + Gdk.keyval_name(keyval).split("_")[0] + ">"
                for keyval in list(set(self.key_unpressed))
            ]
            response_arr.sort(key=lambda i: len(i), reverse=True)
            self.key_combination = "".join(response_arr)
            response = Gtk.ResponseType.ACCEPT
            if "<Shift>" in response_arr and len(response_arr[-1]) <= 1:
                response = Gtk.ResponseType.CANCEL
            if not self.response(response):
                self.destroy()

    def update_label_text(self,):
        # Update the label based on the state of the hit variable
        self.label.set_text("Shortcut pressed %d times" % self.shortcut_hits)
