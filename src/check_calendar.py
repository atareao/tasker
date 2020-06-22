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
from gi.repository import Gtk

try:
    gi.require_version("Gtk", "3.0")
except Exception as e:
    print(e)
    exit(-1)


class CheckCalendar(Gtk.Grid):
    """Docstring for CheckCalendar. """

    def __init__(self, date=None):
        """TODO: to be defined. """
        Gtk.Grid.__init__(self)

        self.expander = Gtk.Expander.new("")
        self.calendar = Gtk.Calendar()
        self.expander.add(self.calendar)
        self.attach(self.expander, 0, 0, 1, 1)

        if date:
            self.set_active(True)
            self.set_date(date)
        else:
            self.set_active(False)

    def set_date(self, date):
        if not date:
            return
        self.expander.set_expanded(True)
        self.calendar.select_month(int(date[5:7]) - 1, int(date[0:4]))
        self.calendar.select_day(int(date[-2:]))

    def get_date(self):
        if self.expander.get_expanded():
            date = self.calendar.get_date()
            return "{:04d}-{:02d}-{:02d}".format(
                date.year, date.month + 1, date.day
            )
        return None

    def set_active(self, active):
        self.expander.set_expanded(active)

    def get_active(self):
        return self.expander.get_expanded()
