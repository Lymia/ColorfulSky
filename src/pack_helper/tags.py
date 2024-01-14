import copy
import json
import os
import os.path

from pack_helper.utils import *

def parse_config(datapack, f, strict = True, no_generate = False, kinds = ["blocks", "items"], ignore_jaopca = False):
    flag_no_generate = no_generate
    flag_override = False
    flag_kinds = kinds
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
                for flag in args:
                    if flag == "NO_GENERATE":
                        flag_no_generate = True
                    elif flag == "OVERRIDE":
                        flag_override = True
                    elif flag == "BLOCK":
                        flag_kinds.append("blocks")
                    elif flag == "ITEM":
                        flag_kinds.append("items")
                    elif flag == "FLUID":
                        flag_kinds.append("fluids")
                    elif flag == "SLURRY":
                        flag_kinds.append("slurries")
                    else:
                        raise Exception(f"Unknown tag flag: {flag}")
                continue
            
            if head == "$clear":
                for kind in flag_kinds:
                    datapack.tags._tags[kind][args[0]].clear()
                continue
            if head == "$copy":
                src = args[0]
                dst = args[1]
                for kind in flag_kinds:
                    datapack.tags._tags[kind][dst] = copy.deepcopy(datapack.tags._tags[kind][src])
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
                tag = args[0]
                if ignore_jaopca and tag.startswith("jaopca:"):
                    continue
                if tag[0] == '!':
                    datapack.tags.remove_tag(flag_kinds, tag[1:], current_tag, generated = not flag_no_generate)
                else:
                    datapack.tags.add_tag(flag_kinds, tag, current_tag, generated = not flag_no_generate)
                continue
            
            if not strict:
                continue
            if head.startswith('//'):
                continue
            if head.strip() == '':
                continue
            raise Exception(f"Tag config parse failure: {line}")
