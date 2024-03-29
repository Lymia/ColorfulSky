import copy
import json
import os
import os.path
import toml

from pack_helper.utils import open_mkdir, js_minify_simple

class DatapackWriter(object):
    def __init__(self, kubejs_dir, config_dir):
        self._kubejs_dir = kubejs_dir
        self._config_dir = config_dir

        self._has_config = set({})
        self._config_toml = {}
        self._config_json = {}

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
    def _write_data(self, name, kind, data):
        self._write_if_not_exists(f"{self._kubejs_dir}/{kind}/{name}", data)

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
    def replace_ingredient(self, src, dst):
        self._replaced_ingredients.append([src, dst])
    def remove_recipe(self, name):
        self._removed_recipes.append(name)

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
        self._write_if_not_exists(f"{self._kubejs_dir}/assets/{name}", json.dumps(json_data, indent = True))
    def add_json_data(self, name, json_data):
        """Adds an JSON data pack file."""
        self._write_if_not_exists(f"{self._kubejs_dir}/data/{name}", json.dumps(json_data, indent = True))

    def add_i18n(self, group, name, value, lang = "en_us"):
        """Adds a translation string to override."""
        self._i18n_strings.setdefault(lang, {}).setdefault(group, {})[name] = value

    def copy_asset(self, dst, src):
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/assets/{dst}", src)
    def write_asset(self, dst, src):
        self._write_if_not_exists(f"{self._kubejs_dir}/assets/{dst}", src)
    def compose_texture(self, target_path, overlay_source, overlay_layer, base_source):
        """Composes a texture using GIMP."""
        overlay = self._gimp_load_xcf(overlay_source)
        base = self._gimp_load_png(base_source)

        target_path = f"{self._kubejs_dir}/assets/{target_path}"

        scope = overlay.mutable_scope()
        target_layer = scope.get_layer_by_name(overlay_layer)
        new_layer = scope.new_layer(parent = target_layer)
        scope.copy_image_to_layer(new_layer, base)

        make_parents(target_path)

        self._gimp_actions.append((scope, target_path, target_layer))

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
        values = sorted(list(set(map(lambda x: (x[:-1], False) if x.endswith("?") else (x, True), values))))
        values = list(map(lambda x: {"id": x[0], "required": False} if not x[1] else x[0], values))
        json_str = json.dumps({
            "replace": override,
            "values": values
        })
        self._write_if_not_exists(f"{self._kubejs_dir}/data/{dir_for_tag(tag, kind)}", json_str)
    def _generate_tags(self, tags):
        for kind in tags._tags:
            for tag in tags._tags[kind]:
                original = tags._original_tags[kind][tag] if tag in tags._original_tags[kind] else set([])
                if tag in tags._should_override or len(tags._tags[kind][tag]) != 0:
                    if original != tags._tags[kind][tag]:
                        if tag not in tags._no_generate:
                            self._generate_tag_file(tag, kind, tags._tags[kind][tag], tag in tags._should_override)

    def _make_remove_unused(self):
        json = f"""
            ({repr(sorted(set(self._removed_names + self._hidden_names)))}).forEach(jei_hide_by_id);
            ({repr(sorted(set(self._removed_names)))}).forEach(mark_as_removed);
            ({repr(sorted(set(self._unified_names)))}).forEach(mark_as_unified);
        """
        self.add_client_script("pack_data", json)

        removed_tags = set({})
        for kind in self.tags._tags:
            for tag in self.tags._tags[kind]:
                if len(self.tags._tags[kind][tag]) == 0:
                    removed_tags.add(f"#{tag}")
        removed_tags = list(removed_tags)

        json = f"""
            ({repr(sorted(set(self._removed_names)))}).forEach(remove_recipe_by_output);
            ({repr(sorted(set(self._removed_names + removed_tags)))}).forEach(remove_recipe_by_item);
            ({repr(sorted(set(self._removed_recipes)))}).forEach(remove_recipe_by_id);
            ({repr(sorted(self._replaced_ingredients))}).forEach(x => replace_ingredient(x[0], x[1]));
        """
        self.add_server_script("pack_data", json)
    def _finalize(self):
        self._generate_tags(self.tags)
        self._make_remove_unused()
        for lang in self._i18n_strings:
            for group in self._i18n_strings[lang]:
                data = json.dumps(self._i18n_strings[lang][group], indent = True)
                self._write_if_not_exists(f"{self._kubejs_dir}/assets/{group}/lang/en_us.json", data)

        # Copy kubejs configuration
        res_dir = f"{os.path.dirname(__file__)}/config"
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/config/client.properties", f"{res_dir}/client.properties")
        self._copy_from_if_not_exists(f"{self._kubejs_dir}/config/common.properties", f"{res_dir}/common.properties")
        self._write_if_not_exists(f"{self._kubejs_dir}/README.md", "See this modpack's repository.")

        # Write generated configuration
        for config in self._config_json:
            self._write_file(f"{self._config_dir}/{config}", json.dumps(self._config_json[config], indent = True))
        for config in self._config_toml:
            self._write_file(f"{self._config_dir}/{config}", toml.dumps(self._config_toml[config]))
