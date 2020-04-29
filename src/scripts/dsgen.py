#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict
import dstypes

from dstypes import *


class DsGen:
    def __init__(self):
        self.classes = OrderedDict()
        self.enums = OrderedDict()
        self.fields = OrderedDict()
        self.arrays = OrderedDict()
        self.ctors = OrderedDict()
        self.class_end = OrderedDict()
        self.assign_func = OrderedDict()
        self.tojson_func = OrderedDict()
        self.enum_names = list()
        self.class_names = list()
        self.o_file = sys.stdout
        self.keywords = ['default', 'class', 'self', 'auto']

    def run(self, ds_list):

        # enum пробегаем отдельно, т.к. у них функции конвертации другие
        for item in ds_list:
            if item.object_type == DSResource.Type.Enum:
                self.enum_names.append(item.name)
            elif item.object_type == DSResource.Type.Object:
                self.class_names.append(item.name)

        for item in ds_list:
            if item.object_type == DSResource.Type.Object:
                self._gen_class(item)
            elif item.object_type == DSResource.Type.Enum:
                self._gen_enum(item)
            elif item.object_type == DSResource.Type.Array:
                self._gen_array(item)

        for key in self.enums.keys():
            self._print(self.enums[key])

        for key in self.arrays.keys():
            self._print(self.arrays[key])

        for key in self.classes.keys():
            self._print(self.classes[key])
            self._print(self.ctors[key])
            self._print(self.fields[key])
            self._print(self.assign_func[key])
            self._print(self.tojson_func[key])
            self._print(self.class_end[key])
            self._print("};")

    def _gen_class(self, item, base_class_name=None):

        all_base_classes = list()

        if item.base_type is not None:
            all_base_classes.append(item.base_type)
        all_base_classes.extend(item.refs)

        base_classes = ', '.join(all_base_classes)
        if len(base_classes) != 0:
            base_classes = ": " + base_classes

        class_begin = "// {0}\nstruct {1}{2} {{".format(item.description, item.name, base_classes)
        if base_class_name is not None:
            self._insert_class_before(base_class_name, item.name, class_begin)
        else:
            self.classes[item.name] = class_begin

        self._gen_ctors(item)
        self._gen_fields(item)
        self._gen_assign(item)
        self._gen_tojson(item)
        self._gen_class_end(item)

    def _gen_tojson(self, item):
        self.tojson_func[item.name] = \
            "    QByteArray toJson() const {\n"\
            "        QByteArray __data;\n"\
            "        QTextStream __out(&__data, QIODevice::WriteOnly);\n"\
            "        return __data;\n" \
            "    }"

    def _gen_assign(self, item):
        self.assign_func[item.name] = "    void assign(const QJsonObject &obj) {\n"\

        for f in item.fields:
            esc_f_name = self._escape_keywords(f.name)
            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Object or \
                    f.type in self.class_names:
                self.assign_func[item.name] += self._tab(2)
                self.assign_func[item.name] += '{1}.assign(obj.value("{0}").toObject());\n'.format(f.name, esc_f_name)
                continue
            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Enum:
                continue

            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Array:
                self.assign_func[item.name] += self._tab(2)
                type = f.type.base_type
                converter = dstypes.FromJsonValueTypeConverter(type)

                self.assign_func[item.name] += 'const QJsonArray __array_{0} = obj.value("{0}").toArray();\n'\
                    '        for (int __i_{0}(0); __i_{0} < __array_{0}.size(); ++__i_{0}) {{\n'\
                    '            {3}.append({1}(__array_{0}.at(__i_{0}).to{2}()));\n'\
                    '        }}\n'.format(f.name, type, converter, esc_f_name)
                continue

            if f.type in self.enum_names:
                self.assign_func[item.name] += self._tab(2)
                self.assign_func[item.name] += '{2} = {0}FromString(obj.value("{1}").toString());\n'.format(f.type, f.name, esc_f_name)
                continue

            self.assign_func[item.name] += self._tab(2) + '{2} = obj.value("{0}").to{1}();\n'.format(f.name, f.to_func(), esc_f_name)

        self.assign_func[item.name] += "    }"

    def _gen_class_end(self, item):
        self.class_end[item.name] = \
            "    bool isNull() const { return is_null_; }\n"\
            "    void setNull(bool null) { is_null_ = null; }\n"\
            "private:\n" \
            "    bool is_null_;"

    def _gen_ctors(self, item):
        self.ctors[item.name] = \
            "    {0}() = default;\n" \
            "    explicit {0}(const QJsonObject &obj): is_null_(obj.isEmpty()) {{ assign(obj); }}".format(item.name)

    def _gen_enum(self, item):

        self.enums[item.name] = 'enum class {0} {{\n'.format(item.name)

        to_string = 'QString {0}ToString({0} value) {{\n'\
            '    switch (value) {{\n'.format(item.name)
        from_string = '{0} {0}FromString(const QString &value) {{\n'.format(item.name)
        for i in range(0, len(item.fields)):
            ef = item.fields[i]
            field = ef.name
            v = ef.name
            if ef.is_number:
                if int(ef.name) < 0:
                    v = "minus" + str(abs(ef.name))
                else:
                    v = "_" + (str(ef.name))
                field = "{0} = {1}".format(v, ef.name)
            comma = "," if not i == len(item.fields) - 1 else ''
            self.enums[item.name] += self._tab() + "{0}{1} // {2}\n".format(field, comma, ef.description)

            to_string += self._tab(2) + 'case {0}::{1}: return QString("{2}");\n'.format(item.name, v, ef.name)
            from_string += self._tab() + 'if (value == "{0}") return {1}::{2};\n'.format(ef.name, item.name, v)

        from_string += \
            '    throw std::invalid_argument('\
            'QString("Invalid argument `%1` for enum {0}").arg(value).toStdString());\n}}\n'.format(item.name)
        to_string += '    }\n    return QString();\n}\n'
        self.enums[item.name] += "};\n"
        self.enums[item.name] += to_string
        self.enums[item.name] += from_string

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

            n = self._escape_keywords(n)
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

    def _escape_keywords(self, name):
        if name in self.keywords:
            return "_" + name
        return name


