import logging

from notion_client import Client
from pprint import pprint
class notion_API():
    def __init__(self):
        self.client = Client(auth="secret_yTKuSw2z5ZTk2UWEmW7wLZ5BCRXxYIA3UlnCYHczuG1", log_level=logging.DEBUG)
        self.pageId = "5132694bff09416884330ab825c1adbb"
        self.tableId = ""

    def create_table(self):
        column_name = ["words", "english meaning", "chinese meaning", "example"]
        cells = [self.set_table_contents(name) for name in column_name]
        children = [{"type": "table",
                     "table": {
                         "table_width": 4,
                         "has_column_header": False,
                         "has_row_header": False,
                         "children": [
                             {"type": "table_row",
                              "table_row": {
                                  "cells": cells}
                              }
                         ]

                     },
                     }]
        create_blocks = dict(self.client.blocks.children.append(self.pageId, children=children))
        result = (dict(create_blocks).get("results"))
        id = (dict(result[0]).get("id"))
        self.tableId = id


    def set_table_contents(self,content):
        cell = [
            {
                "type": "text",
                "text": {
                    "content": f"{content}",
                },
                "annotations": {
                    "color": "default"
                },
                "plain_text": f"{content}",
            }
        ]
        return cell


    def insert_table_row(self,contents):
        cells = [self.set_table_contents(content) for content in contents]
        children = [{"type": "table_row",
                     "table_row": {
                         "cells": cells}}]
        self.client.blocks.children.append(self.tableId, children=children)


    def paragraph_content(self,content, type='paragraph', color="purple"):
        children = {}
        children['type'] = f'{type}'
        paragraph = {}
        rich_text_array = []
        rich_text = {}
        rich_text["type"] = "text"
        rich_text["text"] = {
            "content": f"{content}"}
        rich_text_array.append(rich_text)
        paragraph["rich_text"] = rich_text_array
        paragraph["color"] = f"{color}"
        children[f"{type}"] = paragraph
        data_array = [children]
        self.client.blocks.children.append(self.pageId, children=data_array)



