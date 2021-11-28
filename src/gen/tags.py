import json
import os
import os.path

from gen.utils import *

def parse_config(datapack, f):
    flag_override = False
    flag_block = False
    flag_item = False
    current_tag = None
    
    with open(f, 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            words = line.split(" ")
            head = words[0]
            args = words[1:]
            
            if head.startswith('$'):
                flag_override = False
                flag_block = False
                flag_item = False
                for flag in words:
                    if flag == "OVERRIDE":
                        flag_override = True
                    if flag == "BLOCK":
                        flag_block = True
                    if flag == "ITEM":
                        flag_item = True
                continue
            if head.startswith('#'):
                tag = head[1:]
                if flag_override:
                    datapack.tags.mark_override(tag)
                current_tag = tag
                continue
            if head == '-':
                assert(current_tag != None)
                if flag_block:
                    datapack.tags.add_block_tag(args[0], current_tag)
                if flag_item:
                    datapack.tags.add_item_tag(args[0], current_tag)
                continue
            if head.startswith('//'):
                continue
            if head.strip() == '':
                continue
            
            raise Exception("Tag config parse failure")

def add_from_json(datapack, tag, is_block, json):
    if "replace" in json and json["replace"]:
        datapack.tags.mark_override(tag)
    if "values" in json:
        for name in json["values"]:
            if is_block:
                datapack.tags.add_block_tag(name, tag)
            else:
                datapack.tags.add_item_tag(name, tag)
def generate_group_redirect(datapack, mod, group_from, group_to):
    for model in glob.glob(f"{mod}/data/{group_from}/tags/**/*.json"):
        head_len = len(mod)+6+len(group_from)+1
        tag_type, tag_name = model[head_len+5:-5].split("/", 1)
        full_tag = f"{group_to}:{tag_name}"
        with open(model) as fd:
            data = json.loads(fd.read())

        if tag_type == "blocks":
            add_from_json(datapack, full_tag, True, data)
        if tag_type == "items":
            add_from_json(datapack, full_tag, False, data)
