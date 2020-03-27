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
            if item.object_type == DSResource.Type.Object:
                self._gen_class(item)
            elif item.object_type == DSResource.Type.Enum:
                self._gen_enum(item)

        for key in self.enums.keys():
            self._print(self.enums[key])
            self._print("};")

        for key in self.classes.keys():
            self._print(self.classes[key])
            self._print(self.fields[key])
            self._print("\n};")

    def _gen_class(self, item):

        base_class=''
        if item.base_type is not None:
            base_class = ': public ' + item.base_type
        self.classes[item.name] = "class {0} {1} {{\n".format(item.name, base_class)
        self._gen_fields(item)

    def _gen_enum(self, item):
        self.enums[item.name] = 'enum class {0} {{\n'.format(item.name)

        for ef in item.fields:
            self.enums[item.name] += self._tab() + "{0}, // {1}\n".format(ef.name, ef.description)

    def _gen_fields(self, item):
        self.fields[item.name] = ''
        for f in item.fields:
            if item.object_type == DSResource.Type.Array:
                continue

            t = f.type
            n = f.name

            if isinstance(t, DSResource) and t.object_type == DSResource.Type.Object:
                t.name = item.name + "_" + f.name
                self._gen_class(t)
                t = t.name
            if isinstance(t, DSResource) and t.object_type == DSResource.Type.Enum:
                t.name = item.name + "_" + f.name
                self._gen_enum(t)
                t = t.name

            if isinstance(t, DSResource) and t.object_type == DSResource.Type.Array:
                if t.base_type == 'QString':
                     t = 'QStringList'
                else:
                    if t.base_type is None:
                        #t.name =
                        a = t.fields[0]
                        a.name = item.name + "_"  + f.name
                        self._gen_class(a)
                        t.base_type = a.name

                    t = 'QVector<{}>'.format(t.base_type)

            self.fields[item.name] += self._tab() + "{0} {1}; // {2}\n".format(t, n, f.description)

    def _print(self, *args):
        print(*args, file=self.o_file)

    def _tab(self, count=1):
        return " " * count * 4