#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict
from dstypes import *


class DsGen:
    def __init__(self):
        self.classes = OrderedDict()
        self.enums = OrderedDict()
        self.fields = OrderedDict()
        self.o_file = sys.stdout

    def run(self, ds_list):
        for item in ds_list:
            if item.type == DSResource.Type.Object:
                self._gen_class(item)
            elif item.type == DSResource.Type.Enum:
                self._gen_enum(item)

        for key in self.enums.keys():
            self._print(self.enums[key])
            self._print("};")

        for key in self.classes.keys():
            self._print(self.classes[key])
            self._print(self.fields[key])
            self._print("\n};")


    def _gen_class(self, item):
        self.classes[item.name] = "class {0} {{\n".format(item.name)
        self._gen_fields(item)

    def _gen_enum(self, item):
        self.enums[item.name] = 'enum class {0} {{\n'.format(item.name)

        for ef in item.fields:
            self.enums[item.name] += self._tab() + "{0}, // {1}\n".format(ef.name, ef.description)

    def _gen_fields(self, item):
        self.fields[item.name] = ''
        for f in item.fields:
            t = f.type
            n = f.name
            if t is None:
                if f.value.type == DSResource.Type.Array:
                    if f.value.array_type == 'QString':
                        t = 'QStringList'
                    else:
                        t = 'QVector<{}>'.format(f.value.array_type)
                elif f.value.type == DSResource.Type.Object:
                    t = item.name + "_" + f.name
                    f.value.name = t
                    self._gen_class(f.value)
                elif f.value.type == DSResource.Type.Enum:
                    t = item.name + "_" + f.name
                    f.value.name = t
                    self._gen_enum(f.value)

            self.fields[item.name] += self._tab() + "{0} {1}; // {2}\n".format(t, n, f.description)

    def _print(self, *args):
        print(*args, file=self.o_file)

    def _tab(self, count=1):
        return " " * count * 4