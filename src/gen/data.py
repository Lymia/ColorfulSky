import json
import os
import os.path

from gen.utils import *

class TagConfig(object):
    should_override = set({})
    block_tags = {}
    item_tags = {}
    
    def mark_override(self, tag):
        self.should_override.add(tag)
    def add_block_tag(self, name, tag):
        self.block_tags.setdefault(tag, set({})).add(name)
    def add_item_tag(self, name, tag):
        self.item_tags.setdefault(tag, set({})).add(name)
    def add_both_tag(self, name, tag):
        self.add_block_tag(name, tag)
        self.add_item_tag(name, tag)

class DatapackModel(object):
    tags = TagConfig()
    removed_names = []
    generated_scripts = {}
    generated_models = {}
    
    def _find_name(self, field, prefix, sname, value):
        name = f"{prefix}{sname}"
        i = 0
        while name in field or name.startswith("_"):
            name = f"{prefix}S{i}_{sname}"
            i += 0
        field[name] = value
        return name
    
    def remove_name(self, name):
        self.removed_names.append(name)
    def add_script(self, name, script):
        return self._find_name(self.generated_scripts, "", name, js_minify_simple(f"console.log('Running: {name}.js')\n{script}"))
    def add_model(self, name, model, kind):
        name = self._find_name(self.generated_models, f"{kind}/", name, json.dumps(model))
        if kind == "block":
            namefrag = name[len(kind)+1:]
            self.generated_models[f"item/{namefrag}"] = json.dumps({"parent": f"colorfulsky:block/{namefrag}"})
        return name

def generate_tag_file(tag, kind, values, override, target):
    values = sorted(list(values))
    json_str = json.dumps({
        "replace": override,
        "values": values
    })
    
    target_file = f"{target}/data/{dir_for_tag(tag, kind)}"
    with open_mkdir(target_file) as fd:
        fd.write(json_str)
def generate_tags(tags, target):
    for tag in tags.block_tags:
        generate_tag_file(tag, "blocks", tags.block_tags[tag], tag in tags.should_override, target)
    for tag in tags.item_tags:
        generate_tag_file(tag, "items", tags.item_tags[tag], tag in tags.should_override, target)

def make_remove_unused(datapack, target):
    json = js_minify_simple(f"""
        console.log("Running: _remove_unused.js")
        var all = {repr(datapack.removed_names)}
        var doAll = function(f) {{ all.forEach(f) }}
        onEvent('jei.hide.items', e => {{ doAll(x => e.hide(x)) }})
        onEvent('block.tags', e => {{ e.removeAllTagsFrom(all) }})
        onEvent('item.tags', e => {{ e.removeAllTagsFrom(all) }})
    """, priority = 1000)
    with open_mkdir(f"{target}/startup_scripts/generated/_remove_unused.js") as fd:
        fd.write(json)
    
def generate_datapack_files(datapack, target):
    generate_tags(datapack.tags, target)
    make_remove_unused(datapack, target)
    for name in datapack.generated_scripts:
        with open_mkdir(f"{target}/startup_scripts/generated/{name}.js") as fd:
            fd.write(datapack.generated_scripts[name])
    for name in datapack.generated_models:
        with open_mkdir(f"{target}/assets/colorfulsky/models/{name}.json") as fd:
            fd.write(datapack.generated_models[name])
