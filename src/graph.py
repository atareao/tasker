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

from basegraph import BaseGraph
from config import _


class Graph(BaseGraph):
    def __init__(self, title='', by_project=True):
        if by_project:
            self.group_by = 'projects'
            subtitle = 'By project'
        else:
            self.group_by = 'contexts'
            subtitle = 'By context'
        BaseGraph.__init__(self, title, subtitle)

    def get_keys(self, list_of_todos):
        keys = []
        empty = False
        for todo in list_of_todos:
            if getattr(todo, self.group_by):
                for key in getattr(todo, self.group_by):
                    if key not in keys:
                        keys.append(key)
            else:
                empty = True
        if empty:
            keys.append(_('None'))
        keys.sort()
        return keys

    def get_values(self, keys, plaindata):
        values = []
        for todo in plaindata:
            data = []
            for key in keys:
                if key in getattr(todo, self.group_by):
                    data.append(float(todo.tags.get('total_time', '0')) / 3600.0)
                elif not getattr(todo, self.group_by) and key == _('None'):
                    data.append(float(todo.tags.get('total_time', '0')) / 3600.0)
                else:
                    data.append(0)
            values.append({'name': todo.text, 'data': data})
        return values


if __name__ == '__main__':
    graph = Graph('Testing graph')
    graph.run()
