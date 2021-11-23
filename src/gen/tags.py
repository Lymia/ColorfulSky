import json
import os
import os.path

from gen.utils import *

class TagConfigs(object):
    should_override = set({})
    block_tags = {}
    item_tags = {}

def parse_config(tags, f):
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
                    tags.should_override.add(tag)
                current_tag = tag
                continue
            if head == '-':
                assert(current_tag != None)
                if flag_block:
                    tags.block_tags.setdefault(current_tag, set({})).add(args[0])
                if flag_item:
                    tags.item_tags.setdefault(current_tag, set({})).add(args[0])
                continue
            if head.startswith('//'):
                continue
            if head.strip() == '':
                continue
            
            raise Exception("Tag config parse failure")

def generate_tag_file(tag, kind, values, override, target):
    values = sorted(list(values))
    json_str = json.dumps({
        "replace": override,
        "values": values
    })
    
    target_file = f"{target}{dir_for_tag(tag, kind)}"
    os.makedirs(os.path.dirname(target_file), exist_ok = True)    
    with open(target_file, "w") as fd:
        fd.write(json_str)
    
def generate_tags(tags, target):
    for tag in tags.block_tags:
        generate_tag_file(tag, "blocks", tags.block_tags[tag], tag in tags.should_override, target)
    for tag in tags.item_tags:
        generate_tag_file(tag, "items", tags.item_tags[tag], tag in tags.should_override, target)
        
def generate_group_redirect(group_from, group_to, mod, target):
    for model in glob.glob(f"{mod}/data/{group_from}/tags/**/*.json"):
        head_len = len(mod)+6+len(group_from)+1
        from_tag = model[head_len+5:-5].split("/", 1)[1]
        target_path = f"{target}/data/{group_to}/{model[head_len:]}"

        os.makedirs(os.path.dirname(target_path), exist_ok = True)
        with open(target_path, "w") as fd:
            fd.write(json.dumps({
                "replace": False,
                "values": [f"#{group_from}:{from_tag}"]
            }))
