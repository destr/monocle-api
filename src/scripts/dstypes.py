#!/usr/bin/env python3

from enum import Enum

kTypeMap= {'str': 'QString', 'float' : 'double', 'string': 'QString', 'number': 'int'}

def TypeMap(type_name):
    if type_name in kTypeMap:
        return kTypeMap[type_name]
    return type_name


class ResourceElement:
    def __init__(self, element):
        self.url = element["attributes"]["href"]["content"]
        # TODO use rerfact
        transition = self._find_content(element, "transition")
        # может быть много ответов с разными кодами и разными форматами данных
        httpTransactions = self._find_content(transition, "httpTransaction")

        self.jsonobjs = dict()
        self.ds = None

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
                ds = self._find_content(response, "dataStructure")
                if ds is not None and len(ds) > 0:
                    self.ds = ds[0]

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

    def ds_type(self):
        return self.ds["element"]

    def jsonobj(self, method, code):
        try:
            return self.jsonobjs[(method, code)]
        except KeyError:
            return ''

    def codes(self, m):
        return [code for method, code in self.jsonobjs.keys() if m == method]



class DSField:
    def __init__(self, content):
        c = content["content"]
        self.value = None
        self.type = None
        self.name = c["key"]["content"]
        self.description = None
        if 'meta' in content and 'description' in content["meta"]:
            self.description = content["meta"]["description"]["content"]

        self.value = None

        if 'value' in c:
            if 'content' not in c["value"]:
                # тип данных
                self.type = c["value"]["element"]
                return

            v = c["value"]["content"]
            if isinstance(v, (dict, list)):
                v = DSResource(c["value"])
            else:
                self.type = TypeMap(type(v).__name__)

            self.value = v




class DsEnumField:
    def __init__(self, content):
        self.name = content["content"]
        self.description = None
        if "meta" in content and 'description' in content["meta"]:
            self.description = content['meta']['description']['content']


class DSResource:
    class Type(Enum):
        Unknown = 0
        Object = 1
        Enum = 2
        Array = 3

    def __init__(self, content):
        self.fields = list()
        self.type = DSResource.Type.Unknown
        self.array_type = None
        element = content["element"]
        if element == "object":
            self.type = DSResource.Type.Object
            self._parse_object(content)
        elif element == "enum":
            self.type = DSResource.Type.Enum
            self._parse_enum(content)
        elif element == "array":
            self.type = DSResource.Type.Array
            self._parse_array(content)

    def _parse_object(self, content):
        self._parse_meta(content)
        # члены класса
        for item in content["content"]:
            f = DSField(item)
            self.fields.append(f)

    def _parse_meta(self, content):
        if 'meta' not in content:
            return
        meta = content['meta']
        self.name = meta['id']['content']
        if 'description' in meta:
            self.description = meta['description']['content']

    def _parse_enum(self, content):
        self._parse_meta(content)

        enums = content["attributes"]["enumerations"]["content"]
        for e in enums:
            if 'content' not in e:
                continue

            self.fields.append(DsEnumField(e))

    def _parse_array(self, content):
        item=content["content"][0]
        if item['element'] == "object":
            self.array_type = DSResource(content["content"][0])
        else:
            self.array_type = TypeMap(item["element"])
