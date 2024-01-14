import glob
import importlib.util
import json
import json5
import os.path
import pack_helper.tags
import sys

class _Script(object):
    def __init__(self, mod, py_mod_name, script_file, priority):
        self.mod = mod
        self.py_mod_name = py_mod_name
        self.script_file = script_file
        self.priority = priority

    def execute(self, datapack, moddata):
        spec = importlib.util.spec_from_file_location(self.py_mod_name, self.script_file)
        py_module = importlib.util.module_from_spec(spec)

        py_module.datapack = datapack
        py_module.moddata = moddata
        py_module.mod_path = self.mod.path

        spec.loader.exec_module(py_module)

def _script_name(script_path):
    return script_path.split("/")[-1].split(".")[0]
def _load_py(module, script_path, meta):
    script_name = _script_name(script_path)
    priority = int(meta["priority"]) if "priority" in meta else 0
    return _Script(module, f"modules.{module.module_name}.{script_name}", script_path, priority)
def _script_meta(script_path):
    with open(script_path) as fs:
        script = fs.read()

    meta = {}
    for line in script.split("\n"):
        if line.startswith("#"):
            line = line[1:]
        elif line.startswith("//"):
            line = line[2:]
        else:
            break
        if not ":" in line:
            break

        split = line.strip().split(":")
        meta[split[0].strip()] = split[1].strip()
    return meta

class Module(object):
    def __init__(self, path):
        if path[-1] == "/":
            path = path[:-1]
        self.module_name = os.path.basename(path)
        self.path = path

        self.py_scripts = []
        self.py_init_scripts = []
        self.py_early_scripts = []
        self.py_late_scripts = []

        self.js_client_scripts = []
        self.js_server_scripts = []
        self.js_startup_scripts = []

        self.tags = []

        # Load scripts
        for script in sorted(glob.glob(f"{self.path}/scripts/*")):
            if script.endswith("/__pycache__"):
                continue

            meta = _script_meta(script)
            if script.endswith(".py"):
                if not "timing" in meta or meta["timing"] == "normal":
                    self.py_scripts.append(_load_py(self, script, meta))
                elif meta["timing"] == "init":
                    self.py_init_scripts.append(_load_py(self, script, meta))
                elif meta["timing"] == "early":
                    self.py_early_scripts.append(_load_py(self, script, meta))
                elif meta["timing"] == "late":
                    self.py_late_scripts.append(_load_py(self, script, meta))
                else:
                    timing = meta["timing"]
                    raise Exception(f"Invalid timing: {timing}")
            elif script.endswith(".js"):
                if not "side" in meta or meta["side"] == "common":
                    self.js_client_scripts.append(script)
                    self.js_server_scripts.append(script)
                    self.js_startup_scripts.append(script)
                elif meta["side"] == "client":
                    self.js_client_scripts.append(script)
                elif meta["side"] == "server":
                    self.js_server_scripts.append(script)
                elif meta["side"] == "startup":
                    self.js_startup_scripts.append(script)
                else:
                    side = meta["side"]
                    raise Exception(f"Invalid side: {side}")
            else:
                raise Exception(f"Invalid extension: {script}")

        # Sort python scripts by priority
        self.py_scripts.sort(key = lambda x: (x.priority, x.py_mod_name))
        self.py_init_scripts.sort(key = lambda x: (x.priority, x.py_mod_name))
        self.py_early_scripts.sort(key = lambda x: (x.priority, x.py_mod_name))
        self.py_late_scripts.sort(key = lambda x: (x.priority, x.py_mod_name))

        # Load tags
        for tags_path in glob.glob(f"{self.path}/tags/*.txt"):
            self.tags.append(tags_path)

    def execute_init(self, datapack, moddata):
        sys.path.append(f"{self.path}/path/")
        for script in self.py_init_scripts:
            script.execute(datapack, moddata)

    def execute_early(self, datapack, moddata):
        # Execute any early scripts in the module
        for script in self.py_early_scripts:
            script.execute(datapack, moddata)

        # Load tags
        for tag_file in self.tags:
            print(f"  - Loading tags from '{tag_file}'")
            pack_helper.tags.parse_config(datapack, tag_file)

        # Load toml configuration
        if os.path.exists(f"{self.path}/config"):
            print(f"  - Loading configuration from '{self.path}/config'")
            for short_path, file_path in self.find_all_files("config"):
                datapack._load_toml(short_path, file_path)

    def execute(self, datapack, moddata):
        # Execute any scripts in the module
        for script in self.py_scripts:
            print(f"  - Running '{script.script_file}'...")
            script.execute(datapack, moddata)

        # Copy Javascript scripts
        self._copy_scripts_js(datapack, self.js_client_scripts, "client_scripts")
        self._copy_scripts_js(datapack, self.js_server_scripts, "server_scripts")
        self._copy_scripts_js(datapack, self.js_startup_scripts, "startup_scripts")

        # Copy assets and data
        self._copy_data(datapack, "assets")
        self._copy_data(datapack, "data")

    def execute_late(self, datapack, moddata):
        # Execute any late scripts in the module
        for script in self.py_late_scripts:
            script.execute(datapack, moddata)

    def _copy_data(self, datapack, kind):
        if os.path.exists(f"{self.path}/{kind}"):
            print(f"  - Copying {kind} from '{self.path}/{kind}'")
            for short_path, file_path in self.find_all_files(kind):
                if short_path.endswith(".json") or short_path.endswith(".json5"):
                    # reencode json
                    data = json.dumps(json5.loads(open(file_path).read()), indent = True)
                    datapack._write_data(short_path, kind, data)
                else:
                    datapack._copy_data(short_path, kind, file_path)

    def _copy_scripts_js(self, datapack, target, kind):
        for script_path in target:
            print(f"  - Copying '{script_path}' for '{kind}'")
            script_name = _script_name(script_path)
            datapack._kubejs_copy_script(f"{kind}/{self.module_name}-{script_name}", ".js", script_path)

    def find_all_files(self, kind):
        heading_len = len(f"{self.path}/{kind}/")
        for file_path in glob.glob(f"{self.path}/{kind}/**", recursive = True):
            short_path = file_path[heading_len:]
            if os.path.isfile(file_path):
                yield short_path, file_path

class ModuleLoader(object):
    modules = []

    def __init__(self):
        self.modules.append(Module(f"{os.path.dirname(__file__)}/BaseModule"))
        for script_path in sorted(glob.glob(f"modules/*")):
            self.modules.append(Module(script_path))

    def execute_init(self, datapack, moddata):
        for module in self.modules:
            module.execute_init(datapack, moddata)
    def execute_early(self, datapack, moddata):
        for module in self.modules:
            module.execute_early(datapack, moddata)
    def execute_late(self, datapack, moddata):
        for module in self.modules:
            module.execute_late(datapack, moddata)
    def execute(self, datapack, moddata):
        for module in self.modules:
            module.execute(datapack, moddata)
