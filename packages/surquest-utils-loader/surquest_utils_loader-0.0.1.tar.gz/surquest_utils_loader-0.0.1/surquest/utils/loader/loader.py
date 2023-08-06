#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import json
from collections import OrderedDict


class DictDot(OrderedDict):
    """Dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class YAMLLoader(yaml.FullLoader):

    def construct_yaml_map(self, node):
        data = DictDot()
        yield data
        value = self.construct_mapping(node)
        data.update(value)


YAMLLoader.add_constructor(
    'tag:yaml.org,2002:map',
    YAMLLoader.construct_yaml_map
)


class Loader(object):
    """Loader class helps you to handle inputs from different sources as:
    YAML, JSON, TXT, SQL
    """

    @classmethod
    def load(cls, path, output_type=DictDot):
        """Method loads any type of the file (YAML, JSON) and
        returns it as OrderedDict

        :type path: str
        :param path: path to the file (including file name)

        :type output_type: dict or DictDot
        :param output_type: type of the output object

        :returns: DictDot
        :rtype: DictDot

        :Example:

        ::

            config = Loader.load(path="./config.yaml")

        """

        file_type = path.split(".")[-1]

        if file_type.lower() in ["json"]:
            return cls.load_json(path=path, output_type=output_type)

        if file_type.lower() in ["yaml", "yml"]:
            return cls.load_yaml(path=path, output_type=output_type)

        if file_type.lower() in ["sql", "txt"]:
            return cls.load_txt(path=path)

    @classmethod
    def load_yaml(cls, path, output_type=DictDot):
        """Method loads yaml file and returns it as OrderedDict

        :type path: str
        :param path: path to the file (including file name)

        :type output_type: dict or DictDot
        :param output_type: type of the output object

        :returns: Yaml file content as OrderedDict
        :rtype: collections.OrderedDict

        :Example:

        ::

            config = Loader.load_yaml(path="./config.yaml")

        """

        if output_type == dict:

            with open(path, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)

        else:

            with open(path, 'r') as f:
                config = yaml.load(f, Loader=YAMLLoader)

        return config

    @classmethod
    def load_json(cls, path, output_type=DictDot):
        """Method loads json file and returns it as OrderedDict

        :type path: str
        :param path: path to the file (including file name)

        :type output_type: dict or DictDot
        :param output_type: type of the output object

        :returns: JSON file content as dict
        :rtype: dict

        :Example:

        ::

            config = Loader.load_json(path="./config.yaml")

        """

        if output_type == dict:

            with open(path, 'r') as f:
                config = json.load(f)

        else:

            with open(path, 'r') as f:
                config = json.load(
                    f,
                    object_pairs_hook=DictDot
                )

        return config

    @classmethod
    def load_txt(cls, path):
        """Method loads TXT or SQL files and returns it as string

        :type path: str
        :param path: path to the file (including file name)

        :returns: SQL file content as string
        :rtype: str

        :Example:

        ::

            config = Loader.load_txt(path="./config.sql")

        """

        with open(path, 'r') as f:
            content = f.read()

        return content
