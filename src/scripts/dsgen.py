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
        self.arrays = OrderedDict()
        self.o_file = sys.stdout

    def run(self, ds_list):
        for item in ds_list:
            if item.object_type == DSResource.Type.Object:
                self._gen_class(item)
            elif item.object_type == DSResource.Type.Enum:
                self._gen_enum(item)
            elif item.object_type == DSResource.Type.Array:
                self._gen_array(item)

        for key in self.enums.keys():
            self._print(self.enums[key])
            self._print("};")

        for key in self.arrays.keys():
            self._print(self.arrays[key]);

        for key in self.classes.keys():
            self._print(self.classes[key])
            self._print(self.fields[key])
            self._print("};")

    def _gen_class(self, item, base_class_name=None):

        all_base_classes = list()

        if item.base_type is not None:
            all_base_classes.append(item.base_type)
        all_base_classes.extend(item.refs)

        base_classes = ', '.join(all_base_classes)
        if len(base_classes) != 0:
            base_classes = ": " + base_classes

        class_begin = "struct {0}{1} {{".format(item.name, base_classes)
        if base_class_name is not None:
            self._insert_class_before(base_class_name, item.name, class_begin)
        else:
            self.classes[item.name] = class_begin

        self._gen_fields(item)

    def _gen_enum(self, item):
        self.enums[item.name] = 'enum class {0} {{\n'.format(item.name)

        for i in range(0, len(item.fields)):
            ef = item.fields[i]
            field = ef.name
            if ef.is_number:
                field = "{0}_{1} = {2}".format(item.name, i, ef.name)
            comma = "," if not i == len(item.fields) - 1 else ''
            self.enums[item.name] += self._tab() + "{0}{1} // {2}\n".format(field, comma, ef.description)

    def _gen_array(self, item):
        self.arrays[item.name] = "struct {1};\nusing {0} = QVector<{1}>;\n".format(item.name, item.base_type)

    def _gen_fields(self, item):
        self.fields[item.name] = ''
        for f in item.fields:
            t = f.type
            n = f.name

            if isinstance(t, DSResource) and t.object_type == DSResource.Type.Object:
                t.name = item.name + "_" + f.name
                self._gen_class(t, item.name)
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
                        a = t.fields[0]
                        a.name = item.name + "_" + f.name
                        self._gen_class(a, item.name)
                        t.base_type = a.name

                    t = 'QVector<{}>'.format(t.base_type)

            self.fields[item.name] += self._tab() + "{0} {1}; // {2}\n".format(t, n, f.description)

    def _print(self, *args):
        print(*args, file=self.o_file)

    def _tab(self, count=1):
        return " " * count * 4

    def _insert_class_before(self, before_key, insert_key, insert_value):
        new_classes = OrderedDict()
        for k, v in self.classes.items():
            if k == before_key:
                new_classes[insert_key] = insert_value
            new_classes[k] = v

        self.classes = new_classes
