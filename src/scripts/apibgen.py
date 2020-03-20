#!/usr/bin/env python3

import json
import os
import io
import sys
import datetime
import subprocess
from argparse import ArgumentParser
from jsonprotogen import JsonProtoGen


class ResourceElement:
    def __init__(self, element):
        self.url = element["attributes"]["href"]["content"]
        # TODO use rerfact
        transition = self._find_content(element, "transition")
        # может быть много ответов с разными кодами и разными форматами данных
        httpTransactions = self._find_content(transition, "httpTransaction")
#        httpResponse = self._find_content(httpTransactions, "httpResponse")
#        httpRequest = self._find_content(httpTransactions, "httpRequest")

        self.jsonobjs = dict()

        def add_asset(assets, method, code):
            t = (None, None)
            if len(assets) > 1:
                t = (assets[0]["content"], assets[1]["content"])
            elif assets:
                t = (assets[0]["content"], None)
            else:
                return

            self.jsonobjs[(method, int(code))] = t

        for transaction in httpTransactions:
            # предполагается что всегда есть запрос
            request = self._find_content(transaction, "httpRequest")
            method = request[0]["attributes"]["method"]["content"]
            assets = self._find_content(request, "asset")
            add_asset(assets, method, 0)

            for response in self._find_content(transaction, "httpResponse"):
                code = response["attributes"]["statusCode"]["content"]
                assets = self._find_content(response, "asset")
                add_asset(assets, method, code)

    def _find_content(self, content, name) -> list:
        result = list()
        if isinstance(content, list):
            for item in content:
                result.extend(self._find_content(item, name))
            return result

        if not "content" in content:
            return result

        for e in content["content"]:
            if "element" in e and e["element"] == name:
                result.append(e)
        return result

    def jsonobj(self, method, code):
        try:
            return self.jsonobjs[(method, code)]
        except KeyError:
            return ''

    def codes(self, m):
        return [code for method, code in self.jsonobjs.keys() if m == method]


class MapFile:
    def __init__(self):
        self.map = dict()
        self.r_map = dict()

    def load(self, path):
        with open(path, "r") as f:
            url = ''
            for line in f:
                if line.startswith('#'):
                    continue
                if line.startswith("/"):
                    url = line.strip()
                    continue
                if line.startswith(' '):
                    line = line.strip()

                    pos = None
                    method = 'GET'
                    try:
                        pos = line.rindex('[')
                        method = line[pos + 1:-1]
                    except ValueError:
                        pass

                    key = (method, url)
                    if key not in self.map:
                        self.map[key] = dict()

                    if line.startswith("<") and len(line) > 5:
                        # коды ответов трёхзначный
                        # в Конце строки может быть тип запросв [] скобках
                        self.map[key][int(line[1:4])] = line[5:pos]
                    if line.startswith(">") and len(line) > 3:
                        # post запрос пока всегда 0. Хотя код не нужен вообще.
                        # Возможно придётся сделать для POST PUT разные коды.
                        self.map[key][0] = line[2:pos]

    def classname(self, method, url, code):
        try:
            key = (method, url)
            return self.map[key][code]
        except KeyError:
            return None



class ApibGen:
    def __init__(self):
        self.opts = None
        self.api = dict()
        self.re = dict()
        self.map = MapFile()
        self.out = sys.stdout

    def run(self):
        parser = ArgumentParser(description='API Blueprint file parser')
        parser.add_argument('-i', dest='input_file', action='store', required=True, help="APIB file")
        parser.add_argument('-o', dest='output_file', action='store', help="Output file. Default stdout", default="-")
        parser.add_argument('-m', dest='mapfile', action='store', required=True, help=" Map file")
        parser.add_argument('-t', dest='outtype', action='store',
                            type=JsonProtoGen.OutType, default='cpp', choices=JsonProtoGen.OutType, help='Type outcode')

        self.opts = parser.parse_args()

        if not os.path.exists(self.opts.input_file):
            print("Input file not exists", file=sys.stderr)
            return

        if not os.path.exists(self.opts.mapfile):
            print("Map file not exists", file=sys.stderr)

        self.map.load(self.opts.mapfile)
        self.api = self._drafter()

        out_close = False
        if self.opts.output_file != "-":
            self.out = open(self.opts.output_file, "w")
            out_close = True

        self._out_header()

        for category in self.api["content"][0]["content"]:
            if category["element"] != "category":
                continue
            for resource in category["content"]:
                json_str = ''

                if resource["element"] == "dataStructure":
                    pass

                if resource["element"] == "resource":
                    re = ResourceElement(resource)
                    self.re[re.url] = re
                    print(re.url)

                    for m in ('GET', 'POST', 'PUT', None):
                        for code in re.codes(m):
                            cname = self.map.classname(m, re.url, code)
                            if cname is None:
                                continue

                            jsongen = JsonProtoGen()
                            jsongen.class_name = cname
                            jsongen.outtype = self.opts.outtype

                            json_str, json_schema = re.jsonobj(m, code)
                            jsongen.i_file = io.StringIO(json_str)
                            if json_schema:
                                jsongen.schema_file = io.StringIO(json_schema)

                            jsongen.o_file = self._open_proto_output_file(jsongen.class_name)
                            try:
                                jsongen.process()
                            except json.JSONDecodeError as e:
                                print("%s:1:1: error: Json decode error for URL: %s type `%s': %s"
                                      % (self.opts.input_file, re.url, cname, str(e)), file=sys.stderr)
                                print(json_str)
                                exit(-1)

                            self._out_include(jsongen.class_name)

        if out_close:
            self.out.close()

    def _out_header(self):
        if self.opts.outtype == JsonProtoGen.OutType.CPP:
            self._print("// DO NOT EDIT. AUTOGENERATED from %s at %s\n" % (self.opts.input_file, datetime.datetime.now()))
            self._print("#pragma once")
        else:
            self._print("# DO NOT EDIT. AUTOGENERATED from %s at %s\n" % (self.opts.input_file, datetime.datetime.now()))

    def _out_include(self, class_name):
        if self.opts.outtype == JsonProtoGen.OutType.CPP:
            self._print("#include <%s.hpp>" % class_name)
        else:
            self._print("from apib.%s import *" % class_name)

    def _print(self, *args):
        return print(*args, file=self.out)

    def _open_proto_output_file(self, class_name):
        if self.opts.output_file == "-":
            return sys.stdout

        gendir = os.path.dirname(self.opts.output_file)
        fname = class_name
        if fname.startswith("::"):
            fname = fname[2:]

        ext = None
        if self.opts.outtype == JsonProtoGen.OutType.CPP:
            ext = ".hpp"
        else:
            ext = ".py"

        return open(os.path.join(gendir, fname + ext), "w")

    def _drafter(self) -> dict:
        cmd = ['/usr/local/bin/drafter', '--format=json', self.opts.input_file]

        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as dr:
            data = dr.stdout.read()
            if isinstance(data, (bytes, bytearray)):
                data = data.decode('utf-8')
            return json.loads(data)


if __name__ == "__main__":
    gen = ApibGen()
    gen.run()
