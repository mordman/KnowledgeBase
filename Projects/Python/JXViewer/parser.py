"""Парсеры для JSON и XML файлов."""

import json
import xml.etree.ElementTree as ET


class DataParser:
    """Утилиты для парсинга файлов данных."""

    @staticmethod
    def parse_json(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def parse_xml(filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    @staticmethod
    def get_tag_by_type(value):
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        if isinstance(value, str):
            return "string"
        return "key"