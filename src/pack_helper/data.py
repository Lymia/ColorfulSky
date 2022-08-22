import json
import os
import os.path

from pack_helper.utils import *

class TagConfig(object):
    _should_override = set({})
    _no_generate = set({})
    _tags = {}
    
    def mark_override(self, tag):
        self._should_override.add(tag)
    def mark_no_generate(self, tag):
        self._no_generate.add(tag)
    def force_generate(self, tag):
        self.mark_override(tag)
        if tag in self._no_generate:
            self._no_generate.remove(tag)

    def add_tag(self, kind, name, tag, generated = True):
        if type(kind) == str:
            kind = [kind]
        if type(tag) == str:
            tag = [tag]
        for k in kind:
            for t in tag:
                if generated:
                    if t in self._no_generate:
                        self._no_generate.remove(t)
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
        return self._tags.setdefault(kind, {}).setdefault(tag, set({}))
    
    def remove_name(self, name):
        for kind_name in self._tags:
            kind = self._tags[kind_name]
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
    _removed_names = []
    _unified_names = []
    _hidden_names = []
    _i18n_strings = {}
    
    def __init__(self, kubejs_dir, config_dir, openloader_dir):
        self._kubejs_dir = kubejs_dir
        self._config_dir = config_dir
        self._openloader_dir = openloader_dir
        
    ##
    ## Private methods
    ##
    def _write_if_not_exists(self, path, data):
        if os.path.exists(path):
            raise Exception(f"File '{path}' already exists!")
        with open_mkdir(path) as fd:
            fd.write(data)
    def _generate_script(self, kind, name, script, priority):
        # Minify/process the script
        script = js_minify_simple(script, priority = priority)
        
        # Find an open path for the script
        target_path = f"{self._kubejs_dir}/{kind}/colorfulskies_gen_{name}.js"
        i = 0
        while os.path.exists(target_path):
            target_path = f"{self._kubejs_dir}/{kind}/colorfulskies_gen_{name}_{i}.js"
            i += 1
        
        # Write script to path
        self._write_if_not_exists(target_path, script)

    ##
    ## Public API methods
    ##
    def hide_name(self, name):
        self._hidden_names.append(name)
    def unify_name(self, name):
        self._hidden_names.append(name)
        self._unified_names.append(name)
    def remove_name(self, name):
        self._hidden_names.append(name)
        self._removed_names.append(name)
        self.tags.remove_name(name)
        
    def add_client_script(self, name, script, priority = 0):
        self._generate_script("client_scripts", name, script, priority)
    def add_server_script(self, name, script, priority = 0):
        self._generate_script("server_scripts", name, script, priority)
    def add_startup_script(self, name, script, priority = 0):
        self._generate_script("startup_scripts", name, script, priority)

    def add_json_asset(self, name, json_data):
        self._write_if_not_exists(f"{self._kubejs_dir}/assets/{name}", json.dumps(json_data))
    def add_json_data(self, name, json_data):
        self._write_if_not_exists(f"{self._kubejs_dir}/data/{name}", json.dumps(json_data))
    
    def add_i18n(self, group, name, value):
        self._i18n_strings.setdefault(group, {})[name] = value

    ##
    ## Modpack finalization methods
    ##
    def _generate_tag_file(self, tag, kind, values, override):
        values = sorted(list(values))
        json_str = json.dumps({
            "replace": override,
            "values": values
        })
        self._write_if_not_exists(f"{self._kubejs_dir}/data/{dir_for_tag(tag, kind)}", json_str)
    def _generate_tags(self, tags):
        for kind in tags._tags:
            for tag in tags._tags[kind]:
                if tag in tags._should_override or len(tags._tags[kind][tag]) != 0:
                    if tag not in tags._no_generate:
                        self._generate_tag_file(tag, kind, tags._tags[kind][tag], tag in tags._should_override)
    
    def _make_remove_unused(self):
        json = f"""
            hide_events(false, {repr(sorted(set(self._removed_names)))})
            hide_events(true, {repr(sorted(set(self._hidden_names)))})
            unify_events({repr(sorted(set(self._unified_names)))})
        """
        self.add_client_script("remove_unused", json)
        
        json = f"remove_items({repr(sorted(set(self._removed_names)))})"
        self.add_server_script("remove_unused", json)
    def _finalize(self):
        self._generate_tags(self.tags)
        self._make_remove_unused()
        for group in self._i18n_strings:
            data = json.dumps(self._i18n_strings[group])
            self._write_if_not_exists(f"{self._kubejs_dir}/assets/{group}/lang/en_us.json", data)
