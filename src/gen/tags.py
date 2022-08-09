import json
import os
import os.path

from gen.utils import *

def parse_config(datapack, f, strict = True):
    flag_no_generate = False
    flag_override = False
    flag_kinds = ["blocks", "items"]
    current_tag = None
    
    with open(f, 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            words = line.split(" ")
            head = words[0]
            args = words[1:]
            
            if head == '$flags':
                flag_no_generate = False
                flag_override = False
                flag_kinds.clear()
                for flag in words[1:]:
                    if flag == "NO_GENERATE":
                        flag_no_generate = True
                    elif flag == "OVERRIDE":
                        flag_override = True
                    elif flag == "BLOCK":
                        flag_kinds.append("blocks")
                    elif flag == "ITEM":
                        flag_kinds.append("items")
                    elif flag == "SLURRY":
                        flag_kinds.append("slurries")
                    else:
                        raise Exception(f"Unknown tag flag: {flag}")
                continue
            if head.startswith('#'):
                tag = head[1:]
                if flag_no_generate:
                    datapack.tags.mark_no_generate(tag)
                if flag_override:
                    datapack.tags.mark_override(tag)
                for kind in flag_kinds:
                    datapack.tags.get_tag(kind, tag)
                current_tag = tag
                continue
            if head == '-':
                assert(current_tag != None)
                datapack.tags.add_tag(flag_kinds, args[0], current_tag, generated = not flag_no_generate)
                continue
            
            if not strict:
                continue
            if head.startswith('//'):
                continue
            if head.strip() == '':
                continue
            raise Exception(f"Tag config parse failure: {line}")

def add_from_json(datapack, tag, is_block, json):
    if "replace" in json and json["replace"]:
        datapack.tags.mark_override(tag)
    if "values" in json:
        for name in json["values"]:
            if is_block:
                datapack.tags.add_block_tag(name, tag)
            else:
                datapack.tags.add_item_tag(name, tag)
