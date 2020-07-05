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

import codecs
import json
import os

from config import (
    CONFIG_DIR,
    CONFIG_FILE,
    PARAMS,
    PLUGINS_DIR,
    PLUGINS_INSTALLED_DIR,
)


class Configuration(object):
    def __init__(self):
        self.params = PARAMS
        self.check()
        self.read()
        self.load_plugins()

    def check(self):
        if not os.path.exists(CONFIG_FILE):
            if not os.path.exists(CONFIG_DIR):
                os.makedirs(CONFIG_DIR, 0o700)
            open(CONFIG_FILE, "a").close()
            os.chmod(CONFIG_FILE, 0o600)

    def has(self, key):
        return key in self.params.keys()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError as e:
            print(e)
            self.params[key] = PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        self.params[key] = value

    def reset(self):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        self.params = PARAMS
        self.save()

    def set_defaults(self):
        self.params = PARAMS
        self.save()

    def read(self):
        self.check()
        try:
            f = codecs.open(CONFIG_FILE, "r", "utf-8")
        except IOError as e:
            print(e)
            self.save()
            f = codecs.open(CONFIG_FILE, "r", "utf-8")
        try:
            self.params = json.loads(f.read())
        except ValueError as e:
            print(e)
            self.save()
        f.close()

    def save(self):
        self.check()
        f = codecs.open(CONFIG_FILE, "w", "utf-8")
        f.write(json.dumps(self.params, indent=4, sort_keys=True))
        f.close()

    def __str__(self):
        ans = ""
        for key in sorted(self.params.keys()):
            ans += "{0}: {1}\n".format(key, self.params[key])
        return ans

    def load_plugins(self):
        if not os.path.exists(PLUGINS_DIR):
            os.makedirs(PLUGINS_DIR, 0o700)
        if not os.path.exists(PLUGINS_INSTALLED_DIR):
            os.makedirs(PLUGINS_INSTALLED_DIR, 0o700)

        self._plugins = [
            name
            for name in os.listdir(PLUGINS_INSTALLED_DIR)
            if os.path.isdir(os.path.join(PLUGINS_INSTALLED_DIR, name))
            and "pycache" not in name
            and ".git" not in name
        ]
        self._plugins_to_load = [
            name
            for name in os.listdir(PLUGINS_DIR)
            if os.path.isdir(os.path.join(PLUGINS_DIR, name))
            and "pycache" not in name
            and ".git" not in name
        ]

    def get_plugins(self):
        result = []
        for plugin in self._plugins:
            result.append({"name": plugin, "installed": True})
        for plugin in self._plugins_to_load:
            result.append({"name": plugin, "installed": False})
        result.sort(key=lambda plugin: plugin["name"])
        return result

    def get_plugin_dir(self):
        return PLUGINS_INSTALLED_DIR

    def get_plugin_to_load_dir(self):
        return PLUGINS_DIR
