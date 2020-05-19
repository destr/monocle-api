#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict

from reportlab.lib.validators import _isInt

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
        self.array_names = dict()
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
        self._gen_assign(item, all_base_classes)
        self._gen_tojson(item, all_base_classes)
        self._gen_class_end(item)

    def _gen_tojson(self, item, base_classes=None):
        self.tojson_func[item.name] = \
            "    QByteArray toJson() const {\n"\
            "        QByteArray __data;\n"\
            "        QTextStream __out(&__data, QIODevice::WriteOnly);\n"\
            "        __out.setCodec(\"UTF-8\");\n"\
            '        __out << "{";\n'

        field_count = len(item.fields)
        line_end = ' << ",";\n'
        for f in item.fields:
            field_count -= 1
            if field_count == 0:
                line_end = ';\n'

            esc_f_name = self._escape_keywords(f.name)
            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Object or \
                    f.type in self.class_names:
                self.tojson_func[item.name] += self._tab(2) + '__out << "\\"{1}\\":" << {0}.toJson(){2}'\
                    .format(esc_f_name, f.name, line_end)
                continue

            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Enum:
                continue

            if isinstance(f.type, DSResource) and f.type.object_type == DSResource.Type.Array:
                depth = 1
                type = f.type.base_type
                while isinstance(type, DSResource):
                    depth += 1
                    type = type.base_type

                to_json = '.toJson()' if not IsSimpleType(type) else ''

                self._gen_tojson_array(depth, esc_f_name, f.name, item.name, line_end, to_json)
                continue

            if f.type in self.enum_names:
                self.tojson_func[item.name] += self._tab(2)
                self.tojson_func[item.name] += '__out << "\\"{2}:\\"" << {0}ToString({1}){3}'.format(f.type, esc_f_name, f.name, line_end)
                continue

            if f.type in self.array_names:
                to_json = '.toJson()' if not IsSimpleType(self.array_names[f.type]) else ''
                self._gen_tojson_array(1, esc_f_name, f.name, item.name, line_end, to_json)
                continue

            esc_field = [''] * 2
            if f.type == "QString":
                esc_field[0] = '"\\"" << '
                esc_field[1] = ' << "\\""'

            self.tojson_func[item.name] += self._tab(2) + '__out << "\\"{1}\\":" << {3}{0}{4}{2}'\
                .format(esc_f_name, f.name, line_end, *esc_field)

        self.tojson_func[item.name] += self._tab(2) + '__out << "}";\n'

        self.tojson_func[item.name] += self._tab(2) + "return __data;\n"
        self.tojson_func[item.name] += self._tab() + "}"

    def _gen_tojson_array(self, depth, esc_f_name, f_name, class_name, line_end, to_json):
        for_begin = self._tab(2) + '__out << "\\"{0}\\": [";\n'.format(f_name)
        for_begin += self._tab(2) + "{\n"
        for_begin += self._tab(3) + "const auto &__v_0 = {0};\n".format(esc_f_name)
        for_begin += self._tab(3) + 'for (int i_{0}(0); i_{0} < __v_{0}.size(); ++i_{0}) {{\n'.format(0)
        for_end = ''
        for i in range(1, depth):
            for_begin += self._tab(1 * (i + 3)) + 'const auto &__v_{0} = __v_{1}.at(i_{1});\n'.format(i, i - 1)
            for_begin += self._tab(1 * (i + 3)) + '__out << ((i_{0} == 0) ? "" : ",") << "[";\n'.format(i - 1)
            for_begin += self._tab(1 * (i + 3)) + "for (int i_{0}(0); i_{0} < __v_{0}.size(); ++i_{0}) {{\n".format(i)
            if i == depth - 1:
                for_begin += self._tab(1 * (i + 4)) + \
                             '__out << ((i_{0} == 0) ? "": ",") << __v_{0}.at(i_{0}){1};\n'.format(i, to_json)
            else:
                for_begin += self._tab(1 * (i + 4)) + "const auto &__v_{1} = __v_{0}.at(i_{0});\n".format(i, i + 1)
            for_end += self._tab(1 * (depth - i + 3)) + "}\n"
            for_end += self._tab(1 * (depth - i + 3)) + '__out << "]";\n'
        if depth == 1:
            for_begin += self._tab(4) + '__out << ((i_0 == 0) ? "": ",") << __v_0.at(i_0){0};\n'.format(to_json)
        for_end += self._tab(3) + "}\n"
        for_end += self._tab(2) + "}\n"
        for_end += self._tab(2) + '__out << "]"{0}'.format(line_end)
        self.tojson_func[class_name] += for_begin
        self.tojson_func[class_name] += for_end

    def _gen_assign(self, item, base_classes = None):
        self.assign_func[item.name] = "    void assign(const QJsonObject &obj) { // begin assign func\n"\
        # для базовых классов передаём тот же json
        if base_classes is not None:
            for base_class in base_classes:
                self.assign_func[item.name] += self._tab(2) + "{0}::assign(obj);\n".format(base_class)
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
                depth = 1
                while isinstance(type, DSResource):
                    depth += 1
                    type = type.base_type
                converter = dstypes.FromJsonValueTypeConverter(type)
                self._gen_array_assign(converter, depth, esc_f_name, f.name, item.name, type)

                continue

            if f.type in self.enum_names:
                self.assign_func[item.name] += self._tab(2)
                self.assign_func[item.name] += '{2} = {0}FromString(obj.value("{1}").toString());\n'.format(f.type, f.name, esc_f_name)
                continue

            if f.type not in self.array_names:
                self.assign_func[item.name] += self._tab(2) + '{2} = obj.value("{0}").to{1}();\n'.format(f.name, f.to_func(), esc_f_name)
            else:
                self.assign_func[item.name] += self._tab(2)
                self._gen_array_assign('Object', 1, esc_f_name, f.name, item.name, self.array_names[f.type])

        self.assign_func[item.name] += "    } // assign"

    def _gen_array_assign(self, converter, depth, esc_f_name, f_name, class_name, type):
        for_begin = '{ //for begin scope\n'
        if depth != 1:
            for_begin += 'auto &__v_0 = {0};\n'.format(f_name)

        for_begin += '        const QJsonArray __a_0 = obj.value("{0}").toArray();\n' \
                     '        for (int __i_0(0); __i_0 < __a_0.size(); ++__i_0) {{ // for _0 begin\n'.format(f_name)
        for_end = ''
        i = 0
        for i in range(1, depth):
            for_begin += self._tab(1 * (i + 2))
            for_begin += 'const QJsonArray __a_{0} = __a_{1}.at(__i_{1}).toArray();\n'.format(i, i - 1)
            for_begin += self._tab(1 * (i + 2))
            vector_depth = depth - i
            for_begin += '{0}{1}{2} __v_{3};\n'.format('QVector<' * vector_depth, type, '>' * vector_depth, i)
            for_begin += self._tab(1 * (i + 2))
            for_begin += 'for (int __i_{0}; __i_{0} < __a_{0}.size(); ++__i_{0}) {{\n'.format(i)
            if i == depth - 1:
                for_begin += self._tab(1 * (i + 3))
                for_begin += '__v_{0}.append({1}(__a_{0}.at(__i_{0}).to{2}()));\n'.format(i, type, converter)

            for_end += self._tab(1 * (depth - i + 2)) + '}\n'
            for_end += self._tab(1 * (depth - i + 2)) + '__v_{0}.append(__v_{1});\n'.format(depth - i - 1, depth - i)
        if i == 0:
            for_begin += self._tab(3) + '{3}.append({1}(__a_0.at(__i_{4}).to{2}()));\n' \
                .format(f_name, type, converter, esc_f_name, i)
        for_end += self._tab(2) + '} // for _0 end\n'
        for_end += self._tab(2) + '} // for end scope\n'
        self.assign_func[class_name] += for_begin
        self.assign_func[class_name] += for_end

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
        self.array_names.update({item.name: item.base_type})
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

                    depth = 1
                    while isinstance(t.base_type, DSResource):
                        t = t.base_type
                        depth += 1
                    base_type = t.base_type
                    if t.base_type == 'QString':
                        depth -= 1
                        base_type = 'QStringList'

                    t = '{0}{1}{2}'.format('QVector<' * depth, base_type, '>' * depth)

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



