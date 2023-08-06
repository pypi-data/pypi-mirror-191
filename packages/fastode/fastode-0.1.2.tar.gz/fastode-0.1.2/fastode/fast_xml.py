#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/9/21 16:24
# @Author  : zhangbc0315@outlook.com
# @File    : fast_xml.py
# @Software: PyCharm

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from xml.dom.minidom import Document, Element, Node, Text


class FastXML:

    @classmethod
    def parse_string(cls, xml_str: str) -> Document:
        return parseString(xml_str)

    @classmethod
    def get_els_by_tag_and_attr(cls, el: Element, tag_name: str, attr_key: str, attr_values: [str]):
        for e in el.getElementsByTagName(tag_name):
            if e.getAttribute(attr_key) in attr_values:
                yield e

    @classmethod
    def el_to_texts(cls, el: (Element, Node), res: [] = None) -> [str]:
        res = [] if res is None else res
        for child_el in el.childNodes:
            if isinstance(child_el, Text):
                res.append(child_el.nodeValue)
            else:
                res = cls.el_to_texts(child_el, res)
        return res

    @classmethod
    def _is_leaf_node(cls, node: Node):
        return isinstance(node.firstChild, Text)

    @classmethod
    def get_leaf_nodes(cls, xml, leaf_tags: [str]):
        for child_el in xml.childNodes:
            if cls._is_leaf_node(child_el):
                yield child_el
            elif child_el.tagName in leaf_tags:
                yield child_el
            else:
                for leaf_node in cls.get_leaf_nodes(child_el, leaf_tags):
                    yield leaf_node

    @classmethod
    def get_token_tag_pairs_and_attrs(cls, xml, leaf_tags: [str], attrs: [str]):
        token_tag_pairs = []
        res_attrs = {}
        for attr in attrs:
            res_attrs[attr] = []
        for leaf_node in cls.get_leaf_nodes(xml, leaf_tags):
            texts = cls.el_to_texts(leaf_node)
            token_tag_pairs.append((leaf_node.tagName, ' '.join(texts)))
            for attr in attrs:
                res_attrs[attr].append(leaf_node.getAttribute(attr))
        return token_tag_pairs, res_attrs

    @classmethod
    def xml_to_json(cls, xml):
        res = {}
        for child_el in xml.childNodes:
            if isinstance(child_el, Text):
                return child_el.nodeValue
            else:
                res[child_el.tagName] = cls.xml_to_json(child_el)
        return res

    @classmethod
    def remove_node(cls, node):
        current_node = node
        while True:
            parent_node = current_node.parentNode
            parent_node.removeChild(current_node)
            if len(parent_node.childNodes) > 0:
                break
            current_node = parent_node
        return parent_node

    @classmethod
    def create_node_with_text(cls, xml, tag: str, text: str):
        text_node = xml.createTextNode(text)
        node = xml.createElement(tag)
        node.appendChild(text_node)
        return node


if __name__ == "__main__":
    x = FastXML.parse_string("<root><A><B>b</B><C>c</C></A><A1 upper='A1'>a1</A1></root>")
    print(FastXML.xml_to_json(x))
    print(FastXML.get_token_tag_pairs_and_attrs(x, ['A'], ['upper']))
