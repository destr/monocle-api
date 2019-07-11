#!/usr/bin/env python3

import json
import datetime
import sys
import os
import enum
from collections import OrderedDict
from argparse import ArgumentParser


class EnumDescr:
    def __init__(self, name, items):
        self.name = name
        self.items = items


class JsonProtoGen:
    class OutType(enum.Enum):
        CPP = 'cpp'
        PYTHON = 'py'

    def __init__(self):
        self.opts = None
        self.gen_str = ""
        self.classes = OrderedDict()
        self.assign_func = OrderedDict()
        self.enums = OrderedDict()
        self.enums_from = OrderedDict()
        self.enums_to = OrderedDict()

        self.to_json_func = OrderedDict()
        self.type_map = {'str': 'QString', 'float': 'double'}
        self.to_map = {'int': 'toInt', 'double': 'toDouble', 'QString': 'toString', 'bool': 'toBool'}
        self.keywords = ['default']
        # Костыль поля warm и cold могут быть null. Пока такого костыля достаточно
        self.nullable = ['warm', 'cold']
        self.i_file = sys.stdin
        self.o_file = sys.stdout
        self.class_name = ''
        self.no_ns = False
        self.outtype = JsonProtoGen.OutType.CPP

    def run(self):
        parser = ArgumentParser(description='Generate cpp files from json')
        parser.add_argument('-i', dest='input_file', action='store', help="Json file")
        parser.add_argument('-c', dest='class_name', action='store', help='Class name')
        parser.add_argument('-o', dest='output_file', action='store', help="Output file. Default stdout", default="-")
        parser.add_argument('-t', dest='outtype', action='store',
                            type=JsonProtoGen.OutType, default='cpp', choices=JsonProtoGen.OutType, help='Type outcode')

        self.opts = parser.parse_args()

        i_close = False
        if self.opts.input_file != "-":
            self.class_name = os.path.splitext(os.path.basename(self.opts.input_file))[0]
            self.i_file = open(self.opts.input_file)
            i_close = True

        if self.opts.class_name is not None:
            self.class_name = self.opts.class_name

        o_close = False
        if self.opts.output_file != "-":
            self.o_file = open(self.opts.output_file, "w")
            o_close = True

        self.outtype = self.opts.outtype

        self.process()

        if i_close:
            self.i_file.close()

        if o_close:
            self.o_file.close()

    def process(self):
        if self.class_name.startswith("::"):
            self.class_name = self.class_name[2:]
            self.no_ns = True

        if not self.class_name:
            print("Not set class name", file=sys.stderr)
            return

        j = json.loads(self.i_file.read())

        if self.outtype == JsonProtoGen.OutType.CPP:
            self._process_json_cpp(j, self.class_name)
            self._output_cpp(self.class_name)
        else:
            self._process_json_py(j, self.class_name)
            self._output_py(self.class_name)

    def _add_comments_py(self, class_name, comments):
        self.classes[class_name] += self._tab() + '"""{0}\n    Attributes:\n'.format(class_name)
        for field, comment in comments.items():
            self.classes[class_name] += self._tab(2) + "{0}: {1}".format(field, comment) + "\n"
        self.classes[class_name] += self._tab() + '"""\n\n'

    def _process_json_py(self, json_object, class_name):

        comments = self._extract_field_comments(json_object)

        self.classes[class_name] = "class {0}:\n".format(class_name)

        if comments:
            self._add_comments_py(class_name, comments)

        self.classes[class_name] += self._tab() + "def __init__(self):\n"
        self.assign_func[class_name] = self._tab() + "def fromjson(self, j):\n"
        self.to_json_func[class_name] = self._tab() + """def tojson(self):
        ret = dict()\n"""

        for key in json_object.keys():
            if key.startswith("_comment_"):
                continue

            item = json_object[key]
            if isinstance(item, dict):
                sub_class_name = "st_" + class_name + "_" + key
                self.classes[class_name] += self._tab(2) + "self.{0} = {1}()\n".format(key, sub_class_name)
                self.assign_func[class_name] += self._tab(2) + "self.{0}.fromjson(j['{0}'])\n".format(key)
                self.to_json_func[class_name] += self._tab(2) + "ret[\"{0}\"] = self.{0}.tojson()\n".format(key)
                self._process_json_py(item, sub_class_name)
                continue
            elif isinstance(item, list):
                elem = item[0]
                if isinstance(elem, dict):
                    array_type = class_name + "_" + key
                    self._process_json_py(elem, array_type)

                    self.classes[class_name] += self._tab(2) + "self.{0} = list()\n".format(key)
                    self.assign_func[class_name] += self._tab(2) + """for e in j['{0}']:
            self.{0}.append({1}(e))\n""".format(key, array_type)
                    self.to_json_func[class_name] += self._tab(2) + \
                                                     "ret[\"{0}\"] = [i.tojson() for i in self.items]\n".format(key)
                    continue

            self.classes[class_name] += self._tab(2) + "self.{0} = None\n".format(key)
            self.assign_func[class_name] += self._tab(2) + "self.{0} = j['{0}']\n".format(key)
            self.to_json_func[class_name] += self._tab(2) + "ret[\"{0}\"] = self.{0}\n".format(key)

        self.to_json_func[class_name] += self._tab(2) + "return ret\n"

        self.classes[class_name] += "\n"
        self.classes[class_name] += self.assign_func[class_name]
        self.classes[class_name] += "\n"
        self.classes[class_name] += self.to_json_func[class_name]

    def _output_py(self, root_class_name):
        o_name = self.opts.input_file if self.opts is not None else "-"
        self._print("# DO NOT EDIT. AUTOGENERATED from %s at %s\n" % (o_name, datetime.datetime.now()))
        for k in reversed(list(self.classes.keys())):
            self._print(self.classes[k])
            self._print("\n")

    def _output_cpp(self, root_class_name):

        o_name =  self.opts.input_file if self.opts is not None else "-"
        self._print("// DO NOT EDIT. AUTOGENERATED from %s at %s\n" % (o_name, datetime.datetime.now()))
        self._print("#pragma once")
        for inc in ("QJsonObject", "QJsonArray", "QString", "QVector", "QIODevice", "QTextStream"):
            self._print("#include <QtCore/%s>" % inc)

        self._print("\nnamespace jsonproto {\n")
        # временное  решение. Из разных json иногда получаются одинаковые
        # имена типов (пока вроде с одинаковыми полями). Поэтому нужно будет
        # Генерировать какой-то кеш типов.
        if not self.no_ns:
            self._print("namespace {0} {{\n".format(root_class_name.lower()))

        for k in reversed(list(self.classes.keys())):
            self._print(self.classes[k])

        if not self.no_ns:
            self._print("}\n")
        self._print("}")

    def _process_json_cpp(self, json_object, class_name):
        self.classes[class_name] = """struct {0} {{
    {0}() = default;
    explicit {0}(const QJsonObject &obj) : is_null_(obj.isEmpty()) {{ assign(obj); }}\n""".format(class_name)
        self.assign_func[class_name] = "void assign(const QJsonObject &obj) {\n"
        self.to_json_func[class_name] = """QByteArray toJson() const {
        QByteArray __data;
        QTextStream out(&__data, QIODevice::WriteOnly);
        out.setCodec("UTF-8");
        out << "{";\n"""
        first = True
        comments = self._extract_field_comments(json_object)
        enums = self._extract_field_enums(json_object)

        # генерация объявлений enum
        self.classes[class_name] += self._generate_enums_cpp(class_name, enums)

        for key in json_object.keys():

            if key.startswith("_comment_") or key.startswith("_enum_"):
                continue

            key_esc = self._escape_cpp_keyword(key)
            if first:
                first = False
            else:
                self.to_json_func[class_name] += " << \",\";\n"
            item = json_object[key]
            # с++ объекты, имя нового типа формируется как st_<название поля>, если данный тип уже был, то вначало
            # добавляется имя текущего типа
            if isinstance(item, dict):
                sub_class_name = "st_" + key
                if sub_class_name in self.classes:
                    sub_class_name = class_name + "_st_" + key

                self._add_field(class_name, sub_class_name, key_esc, comments=comments)
                self.assign_func[class_name] += self._tab(2) + '{0}.assign(obj.value("{0}").toObject());\n'.format(key)
                self.to_json_func[class_name] += self._tab(2) + 'out << "\\"{0}\\": " << {0}.toJson()'.format(key)
                self._process_json_cpp(item, sub_class_name)
                continue
            # генерация c++ массиовов
            elif isinstance(item, list):
                elem = item[0]

                # определяем глубину вложнных массивов
                list_depth = 0
                while isinstance(elem, list):
                    elem = elem[0]
                    list_depth += 1

                # C++ тип элемента массива
                array_elem_type = self._type(type(elem).__name__)
                string_list = array_elem_type == "QString"

                user_type = False
                # все словари это другие объекты сгенерированные нами и у них вызываем toJson и assign
                if isinstance(elem, dict):
                    array_elem_type = class_name + "_" + key
                    user_type = True
                    self._process_json_cpp(elem, array_elem_type)

                self._add_field(class_name, self._cpp_array_type(list_depth, array_elem_type, string_list), key_esc,
                                comments=comments)

                assign_for = [''] * (list_depth + 1)
                assign_end = [''] * (list_depth + 1)
                assign_for[0] = self._tab(2) + 'const QJsonArray a = obj.value("{0}").toArray();\n'.format(key)
                assign_for[0] += self._tab(2) + "for (const QJsonValue v0 : a) {\n"

                to_json_for = [''] * (list_depth + 1)
                to_json_end = [''] * (list_depth + 1)

                to_json_for[0] = self._tab(2) + 'const auto &v0 = {};\n'.format(key)
                to_json_for[0] += self._tab(2) + 'for(int i_0(0); i_0 < v0.size(); ++i_0) {\n'

                counter = 0
                # генерируем циклы присваивающие из json в с++ массивы
                while list_depth > 0:
                    counter += 1

                    list_depth -= 1
                    list_type = self._cpp_array_type(list_depth, array_elem_type, string_list)
                    t = 2 + counter
                    assign_for[counter] = self._tab(t) + "{0} __inner{1};\n".format(list_type, counter)
                    assign_for[counter] += self._tab(t) + "for (const QJsonValue v{0}: v{1}.toArray()){{\n"\
                        .format(counter, counter - 1)
                    assign_end[counter] += self._tab(t) + "}\n"

                    if counter != 1:
                        assign_end[counter] += self._tab(t) + "__inner{0}.push_back(__inner{1});\n".format(counter - 1, counter)

                    to_json_for[counter] = self._tab(t) + "const {0} &v{1} = v{2}.at(i_{2});\n"\
                        .format(list_type, counter, counter - 1)
                    to_json_for[counter] += self._tab(t) + 'out << ((i_{0} == 0) ? "[" : ",[");\n'.format(counter - 1)
                    to_json_for[counter] += self._tab(t) + "for (int i_{0}(0); i_{0} < v{0}.size(); ++i_{0}) {{\n".format(counter)

                    to_json_end[counter] = self._tab(t) + "}\n"
                    to_json_end[counter] += self._tab(t) + 'out << "]";\n'

                    if list_depth == 0:
                        assign_for[counter] += self._tab(t + 1) + '__inner{0}.push_back({1}(v{3}.{2}()));\n'\
                            .format(counter, array_elem_type, self._to(array_elem_type), counter)

                        to_json_for[counter] += self._tab(t + 1) + self._output_array_element_to_json(counter, user_type, string_list)

                assign_end[0] += self._tab(3)
                if counter != 0:
                    assign_end[0] += '{0}.push_back(__inner1);\n'.format(key)
                else:
                    assign_end[0] += '{0}.push_back({1}(v0.{2}()));\n'.format(
                        key, array_elem_type, self._to(array_elem_type), counter)

                    to_json_end[0] += self._tab(3) + self._output_array_element_to_json(counter, user_type, string_list)

                assign_end[0] += self._tab(2) + "}\n"
                to_json_end[0] += self._tab(2) + "}\n"

                # объединине функций assign в рабочий с++ код
                self.assign_func[class_name] += self._tab(2) + "{\n"
                self.assign_func[class_name] += '\n'.join(assign_for)
                self.assign_func[class_name] += '\n'.join(reversed(assign_end))
                self.assign_func[class_name] += self._tab(2) + "}\n"

                # объединение функцийй toJson в рабочий код
                self.to_json_func[class_name] += self._tab(2) + 'out << "\\"{0}\\": [";\n'.format(key)
                self.to_json_func[class_name] += self._tab(2) + "{\n"
                self.to_json_func[class_name] += '\n'.join(to_json_for)
                self.to_json_func[class_name] += '\n'.join(reversed(to_json_end))
                self.to_json_func[class_name] += self._tab(2) + "}\n"
                self.to_json_func[class_name] += self._tab(2) + 'out << "]"'

                continue

            t = self._type(type(item).__name__)
            is_nullable = key in self.nullable

            self._add_field(class_name, t, key_esc, is_nullable=is_nullable, comments=comments, enums=enums)
            to_func = "." + self._to(t) + "()"
            if is_nullable:
                to_func = ""

            to_enum = [''] * 2
            from_enum = [''] * 2
            is_enum = key_esc in enums
            if is_enum:
                e_name = enums[key_esc].name
                to_enum[0] = "{0}FromString(".format(e_name)
                to_enum[1] = ")"

                from_enum[0] = "{0}ToString(".format(e_name)
                from_enum[1] = ")"

            self.assign_func[class_name] += self._tab(2) + '{0} = {3}obj.value("{1}"){2}{4};\n'.format(key_esc, key, to_func, *to_enum)

            is_string = (t == 'QString')
            value = key_esc

            if is_nullable:
                value = "({0}.isNull() ? \"null\" : QString::number({0}.{1}()))".format(value, self._to(t))

            if t == 'bool':
                value = '({0} ? "true" : "false")'.format(key_esc)

            if is_enum:
                value = from_enum[0] + value + from_enum[1]
            self.to_json_func[class_name] += self._tab(2) + \
                'out << "\\"{0}\\": " << {1}'.format(key, self._quote_json_string(value, is_string))

        self.assign_func[class_name] += self._tab() + "}\n"
        self.to_json_func[class_name] += ";\n" + self._tab(2) + "out << \"}\";\n"
        self.to_json_func[class_name] += self._tab(2) + "return __data;\n    }\n"



        self.classes[class_name] += self._tab() + self.assign_func[class_name]
        self.classes[class_name] += self._tab() + self.to_json_func[class_name]


        # дополнительные статичные методы
        self.classes[class_name] += """
    bool isNull() const { return is_null_; }
private:
    bool is_null_ = true;
"""
        self.classes[class_name] += self.enums_from[class_name]
        self.classes[class_name] += self.enums_to[class_name]
        self.classes[class_name] += "};\n"

    def _generate_enums_cpp(self, class_name, enums):
        self.enums[class_name] = ''
        self.enums_from[class_name] = ''
        self.enums_to[class_name] = ''

        for n, e in enums.items():
            self.enums[class_name] += self._tab() + "enum {0} {{\n".format(e.name)
            self.enums_from[class_name] += self._tab() + "static {0} {0}FromString(QString str){{\n".format(e.name)
            self.enums_to[class_name] += self._tab() + """static QString {0}ToString(Command cmd){{
        switch (cmd) {{
""".format(e.name)

            is_first = True
            for key, value, text_value in e.items:
                if is_first:
                    is_first = False
                else:
                    self.enums[class_name] += ",\n"
                self.enums[class_name] += self._tab(2) + "{0} = {1}".format(key, value)
                self.enums_from[class_name] += self._tab(2) + "if (str == \"{0}\") return {1};\n".format(text_value, key)
                self.enums_to[class_name] += self._tab(3) + "case {0}: return \"{1}\";\n".format(key, text_value)

            self.enums_from[class_name] += self._tab(2) + "return Undefined;\n" + self._tab() + "}\n"
            self.enums_to[class_name] += self._tab(2) + "}\n" + self._tab(2) + "return \"undefined\";\n" + self._tab() + "}\n"
            self.enums[class_name] += "\n" + self._tab() + "};\n"

        return self.enums[class_name]

    def _output_array_element_to_json(self, counter, user_type, string_list):
        obj_to = ''
        if user_type:
            obj_to = '.toJson()'

        field = "v{0}.at(i_{0}){1}".format(counter, obj_to)
        return 'out << ((i_{0} == 0) ? "" : ",") << {1};\n'\
            .format(counter, self._quote_json_string(field, string_list))

    def _quote_json_string(self, field, is_string):
        quotes = [''] * 2
        if is_string:
            quotes[0] = '"\\"" << '
            quotes[1] = ' << "\\""'

        return quotes[0] + field + quotes[1]

    def _cpp_array_type(self, depth, elem_type, is_string_list=False):
        # если итоговый тип элемента массива не строка, то генерируем сразу все вектора
        if not is_string_list:
            depth += 1

        list_depth_open = "QVector<" * depth
        list_depth_close = ">" * depth

        if is_string_list:
            list_depth_open += "QList<"
            list_depth_close += ">"

        return list_depth_open + elem_type + list_depth_close

    def _tab(self, count=1):
        return " " * count * 4

    def _type(self, t):
        if t in self.type_map:
            return self.type_map[t]
        return t

    def _print(self, *args):
        print(*args, file=self.o_file)

    def _add_field(self, class_name, type, name, ident=1, is_nullable = False, comments=dict(), enums=dict()):
        t = type
        if is_nullable:
            t = 'QVariant'
        if name in comments:
            self.classes[class_name] += self._tab(ident) + "// " + comments[name] + "\n"

        if name in enums:
            t = enums[name].name

        self.classes[class_name] += self._tab(ident) + t + " " + name + ";\n"

    def _to(self, type):
        if type in self.to_map:
            return self.to_map[type]
        return "toObject"

    def _escape_cpp_keyword(self, word):
        """ Маскировка ключевых слов C++
        :param word:
        :return:
        """
        if word in self.keywords:
            return word + "_esc"
        return word

    def _extract_field_comments(self, json_object):
        return self._extract_field_property(json_object, "_comment_")

    def _extract_field_enums(self, json_object):
        enums = self._extract_field_property(json_object, "_enum_")
        # разбор строковой записи enum
        # <имя_перечисления>: ключ=значение/текстовое_значение,...
        for key, value in enums.items():
            index = value.index(':')
            enum_name = value[0:index]

            str_items = value[index + 1:].split(",")
            items = self._parse_enum_items(str_items)
            enums[key] = EnumDescr(enum_name, items)

        return enums

    def _parse_enum_items(self, items):
        r = list()
        max_value = -sys.maxsize
        for i in items:
            key, value = i.split('=', maxsplit=2)
            key = key.strip()
            i_val, t_val = value.split('/', maxsplit=2)
            i_val = i_val.strip()
            t_val= t_val.strip()

            max_value = max(max_value, int(i_val, 0))

            r.append((key, i_val, t_val))

        # добавляем Undefined
        r.append(("Undefined", max_value + 1, "undefined"))

        return r

    def _extract_field_property(self, json_object, property):
        """
        Извлечение свойств полей имеющих формат <property><field_name>
        :param json_object:
        :param property: имя свойства
        :return:
        """

        p = dict()
        for key in json_object.keys():
            if key.startswith(property):
                field = key[key.index('_', 1) + 1:]
                p[self._escape_cpp_keyword(field)] = json_object[key]

        return p


if __name__ == "__main__":

    jpg = JsonProtoGen()
    jpg.run()

