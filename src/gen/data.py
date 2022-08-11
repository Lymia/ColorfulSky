import json
import os
import os.path

from gen.utils import *

class TagConfig(object):
    should_override = set({})
    no_generate = set({})
    tags = {}
    
    def mark_override(self, tag):
        self.should_override.add(tag)
    def mark_no_generate(self, tag):
        self.no_generate.add(tag)
    def force_generate(self, tag):
        if tag in self.no_generate:
            self.no_generate.remove(tag)
        
        
    def add_tag(self, kind, name, tag, generated = True):
        if type(kind) == str:
            kind = [kind]
        if type(tag) == str:
            tag = [tag]
        for k in kind:
            for t in tag:
                if generated:
                    if t in self.no_generate:
                        self.no_generate.remove(t)
                self.get_tag(k, t).add(name)
    def remove_tag(self, kind, name, tag, generated = True):
        if type(kind) == str:
            kind = [kind]
        if type(tag) == str:
            tag = [tag]
        for t in tag:
            for k in kind:
                tag_data = self.get_tag(k, t)
                if name in tag_data:
                    if generated:
                        self.force_generate(t)
                    tag_data.remove(name)
    def get_tag(self, kind, tag):
        assert(tag != None)
        return self.tags.setdefault(kind, {}).setdefault(tag, set({}))
    
    def remove_name(self, name):
        for kind_name in self.tags:
            kind = self.tags[kind_name]
            for tag in kind:
                tag_data = kind[tag]
                if name in tag_data:
                    self.force_generate(tag)
                    tag_data.remove(name)
        
    def get_block_tag(self, tag):
        return self.get_tag("blocks", tag)
    def get_item_tag(self, tag):
        return self.get_tag("items", tag)

    def add_block_tag(self, name, tag):
        self.add_tag("blocks", name, tag)
    def add_item_tag(self, name, tag):
        self.add_tag("items", name, tag)
    def add_both_tag(self, name, tag):
        self.add_tag(["blocks", "items"], name, tag)

class DatapackModel(object):
    tags = TagConfig()
    removed_names = []
    generated_scripts = {}
    generated_server_scripts = {}
    generated_client_scripts = {}
    i18n_strings = {}
    textures = {}
    new_files = {}
    
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
        self.tags.remove_name(name)
        
    def process_script(self, name, script):
        return js_minify_simple(script)
    def add_client_script(self, name, script):
        return self._find_name(self.generated_client_scripts, "", name, self.process_script(name, script))
    def add_server_script(self, name, script):
        return self._find_name(self.generated_server_scripts, "", name, self.process_script(name, script))
    def add_script(self, name, script):
        return self._find_name(self.generated_scripts, "", name, self.process_script(name, script))
    
    def add_i18n(self, group, name, value):
        self.i18n_strings.setdefault(group, {})[name] = value
    def add_json_asset(self, name, json_data):
        name = "assets/" + name
        self.new_files[name] = json.dumps(json_data)
    def add_json_data(self, name, json_data):
        name = "data/" + name
        self.new_files[name] = json.dumps(json_data)

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
    for kind in tags.tags:
        for tag in tags.tags[kind]:
            if tag in tags.should_override or len(tags.tags[kind][tag]) != 0:
                if tag not in tags.no_generate:
                    generate_tag_file(tag, kind, tags.tags[kind][tag], tag in tags.should_override, target)

def make_remove_unused(datapack, target):
    json = js_minify_simple(f"hide_events({repr(sorted(set(datapack.removed_names)))})", priority = 1000)
    with open_mkdir(f"{target}/client_scripts/generated_remove_unused.js") as fd:
        fd.write(json)
    json = js_minify_simple(f"remove_items({repr(sorted(set(datapack.removed_names)))})", priority = 1000)
    with open_mkdir(f"{target}/server_scripts/generated_remove_unused.js") as fd:
        fd.write(json)
    
def generate_datapack_files(datapack, target):
    generate_tags(datapack.tags, target)
    make_remove_unused(datapack, target)
    for group in datapack.i18n_strings:
        with open_mkdir(f"{target}/assets/{group}/lang/en_us.json") as fd:
            fd.write(json.dumps(datapack.i18n_strings[group]))
    for name in datapack.generated_scripts:
        with open_mkdir(f"{target}/startup_scripts/generated_{name}.js") as fd:
            fd.write(datapack.generated_scripts[name])
    for name in datapack.generated_server_scripts:
        with open_mkdir(f"{target}/server_scripts/generated_{name}.js") as fd:
            fd.write(datapack.generated_server_scripts[name])
    for name in datapack.generated_client_scripts:
        with open_mkdir(f"{target}/client_scripts/generated_{name}.js") as fd:
            fd.write(datapack.generated_client_scripts[name])
    for name in datapack.new_files:
        with open_mkdir(f"{target}/{name}") as fd:
            fd.write(datapack.new_files[name])
