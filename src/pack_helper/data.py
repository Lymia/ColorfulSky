import json
import os
import os.path
import toml

from pack_helper.gimp import *
from pack_helper.utils import *

class TagConfig(object):
    def __init__(self):
        self._should_override = set({})
        self._no_generate = set({})
        self._tags = {}

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
    def get_fluid_tag(self, tag):
        return self.get_tag("fluids", tag)

    def add_block_tag(self, name, tag):
        self.add_tag("blocks", name, tag)
    def add_item_tag(self, name, tag):
        self.add_tag("items", name, tag)
    def add_both_tag(self, name, tag):
        self.add_tag(["blocks", "items"], name, tag)

class DatapackModel(object):
    def __init__(self, kubejs_dir, config_dir, openloader_dir):
        self._kubejs_dir = kubejs_dir
        self._config_dir = config_dir
        self._openloader_dir = openloader_dir

        self.tags = TagConfig()
        self._removed_names = []
        self._unified_names = []
        self._hidden_names = []
        self._i18n_strings = {}

        self._has_config = set([])
        self._config_toml = {}
        self._config_json = {}

        self._gimp_loaded = {}
        self._gimp_actions = []

    ##
    ## Private methods
    ##
    def _write_file(self, path, data):
        with open_mkdir(path, mode = "wb" if type(data) == bytes else "w") as fd:
            fd.write(data)
    def _write_if_not_exists(self, path, data):
        if os.path.exists(path):
            raise Exception(f"File '{path}' already exists!")
        self._write_file(path, data)
    def _write_maybe_rename(self, prefix, extension, data):
        target_path = f"{prefix}{extension}"
        i = 0
        while os.path.exists(target_path):
            target_path = f"{prefix}_{i}{extension}"
            i += 1
        self._write_if_not_exists(target_path, data)
    def _generate_script(self, kind, name, script, priority):
        script = js_minify_simple(script, priority = priority)
        self._write_maybe_rename(f"{self._kubejs_dir}/{kind}/Generated-{name}", ".js", script)

    def _copy_from_if_not_exists(self, path, source):
        with open(source, "rb") as fd:
            data = fd.read()
        self._write_if_not_exists(path, data)
    def _copy_from_maybe_rename(self, prefix, extension, source):
        with open(source, "rb") as fd:
            data = fd.read()
        self._write_maybe_rename(prefix, extension, data)

    def _gimp_load_xcf(self, path):
        return self._gimp_loaded.setdefault(path, GimpImageElement.load_xcf(path))
    def _gimp_load_png(self, path):
        return self._gimp_loaded.setdefault(path, GimpImageElement.load_png(path))

    def _mark_config_exists(self, path):
        if path in self._has_config:
            raise Exception(f"Attempted to add configuration file '{path}' multiple times.")
        self._has_config.add(path)

    ##
    ## Private API methods
    ##
    def _kubejs_copy_script(self, prefix, extension, source):
        self._copy_from_maybe_rename(f"{self._kubejs_dir}/{prefix}", extension, source)
    def _copy_data(self, name, kind, source):
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/{kind}/{name}", source)

    def _load_toml(self, short_name, source):
        self._mark_config_exists(short_name)
        with open(source, "r") as fd:
            toml_source = fd.read()
        self._config_toml[short_name] = toml.loads(toml_source)
    def _load_json(self, short_name, source):
        self._mark_config_exists(short_name)
        with open(source, "r") as fd:
            json_source = fd.read()
        self._config_json[short_name] = json.loads(json_source)

    ##
    ## Public API methods
    ##
    def hide_name(self, name):
        """Hides an item/block from JEI."""
        self._hidden_names.append(name)
    def unify_name(self, name):
        """Marks an item/block as being unified with another."""
        self._hidden_names.append(name)
        self._unified_names.append(name)
    def remove_name(self, name):
        """Marks an item/block as being removed entirely from the modpack."""
        self._hidden_names.append(name)
        self._removed_names.append(name)
        self.tags.remove_name(name)

    def add_client_script(self, name, script, priority = 0):
        """Adds a KubeJS client script."""
        self._generate_script("client_scripts", name, script, priority)
    def add_server_script(self, name, script, priority = 0):
        """Adds a KubeJS server script."""
        self._generate_script("server_scripts", name, script, priority)
    def add_startup_script(self, name, script, priority = 0):
        """Adds a KubeJS startup script."""
        self._generate_script("startup_scripts", name, script, priority)

    def add_json_asset(self, name, json_data):
        """Adds an JSON resource pack file."""
        self._write_if_not_exists(f"{self._kubejs_dir}/assets/{name}", json.dumps(json_data))
    def add_json_data(self, name, json_data):
        """Adds an JSON data pack file."""
        self._write_if_not_exists(f"{self._kubejs_dir}/data/{name}", json.dumps(json_data))

    def add_i18n(self, group, name, value, lang = "en_us"):
        """Adds a translation string to override."""
        self._i18n_strings.setdefault(lang, {}).setdefault(group, {})[name] = value

    def compose_texture(self, target_path, overlay_source, overlay_layer, base_source):
        """Composes a texture using GIMP."""
        overlay = self._gimp_load_xcf(overlay_source)
        base = self._gimp_load_png(base_source)

        scope = overlay.mutable_scope()
        target = scope.get_layer_by_name(overlay_layer)
        new_layer = scope.new_layer(parent = target)
        scope.copy_image_to_layer(new_layer, base)
        scope.save_png(f"{self._kubejs_dir}/assets/{target_path}", layer = target)
        scope.delete_layer(new_layer)

        self._gimp_actions.append(scope)

    def get_json_config(self, path, create = False):
        """Returns a mutable object containing a JSON configuration file."""
        if create and not path in self._config_json:
            self._mark_config_exists(path)
            self._config_json[path] = {}
        return self._config_json[path]
    def get_toml_config(self, path, create = False):
        """Returns a mutable object containing a TOML configuration file."""
        if create and not path in self._config_toml:
            self._mark_config_exists(path)
            self._config_toml[path] = {}
        return self._config_toml[path]

    ##
    ## Modpack finalization methods
    ##
    def _finalize_gimp(self, gimp, max_processes = 16, process_chunk = None):
        gimp.execute_actions(self._gimp_actions)
        self._gimp_actions = []

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
        for lang in self._i18n_strings:
            for group in self._i18n_strings[lang]:
                data = json.dumps(self._i18n_strings[lang][group])
                self._write_if_not_exists(f"{self._kubejs_dir}/assets/{group}/lang/en_us.json", data)

        # Copy kubejs configuration
        res_dir = f"{os.path.dirname(__file__)}/config"
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/config/client.properties", f"{res_dir}/client.properties")
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/config/common.properties", f"{res_dir}/common.properties")
        self._write_if_not_exists(f"{self._kubejs_dir}/README.md", "See this modpack's repository.")

        # Write generated configuration
        for config in self._config_json:
            self._write_file(f"{self._config_dir}/{config}", json.dumps(self._config_json[config]))
        for config in self._config_toml:
            self._write_file(f"{self._config_dir}/{config}", toml.dumps(self._config_toml[config]))
