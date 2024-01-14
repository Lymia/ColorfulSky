import glob
import importlib.util
import json
import json5
import os.path
import pack_helper.tags
import sys

class Script(object):
    def __init__(self, mod, py_mod_name, script_file):
        self.mod = mod
        self.py_mod_name = py_mod_name
        self.script_file = script_file
        
    def execute(self, datapack, moddata):
        spec = importlib.util.spec_from_file_location(self.py_mod_name, self.script_file)
        py_module = importlib.util.module_from_spec(spec)
        
        py_module.datapack = datapack
        py_module.moddata = moddata
        py_module.mod_path = self.mod.path
        
        spec.loader.exec_module(py_module)

class Module(object):
    def __init__(self, path):
        if path[-1] == "/":
            path = path[:-1]
        self.module_name = os.path.basename(path)
        self.path = path
        
        self.py_scripts = []
        self.py_init_scripts = []
        self.py_late_scripts = []
        
        self.js_common_scripts = []
        self.js_client_scripts = []
        self.js_server_scripts = []
        self.js_startup_scripts = []
        
        self.tags = []
        
        # Load Python scripts
        self._load_scripts_py(self.py_scripts, "py_scripts")
        self._load_scripts_py(self.py_init_scripts, "py_init_scripts")
        self._load_scripts_py(self.py_late_scripts, "py_late_scripts")
        
        # Load KubeJS scripts
        self._load_scripts_js(self.js_common_scripts, "common_scripts")
        self._load_scripts_js(self.js_client_scripts, "client_scripts")
        self._load_scripts_js(self.js_server_scripts, "server_scripts")
        self._load_scripts_js(self.js_startup_scripts, "startup_scripts")
        
        # Load tags
        for tags_path in glob.glob(f"{self.path}/tags/*.txt"):
            self.tags.append(tags_path)
            
    def _load_scripts_py(self, target, kind):
        for script_path in glob.glob(f"{self.path}/{kind}/*.py"):
            script_name = os.path.basename(script_path)[:-3]
            target.append(Script(self, f"modules.{self.module_name}.{script_name}", script_path))
    def _load_scripts_js(self, target, kind):
        for script_path in glob.glob(f"{self.path}/{kind}/*.js"):
            script_name = os.path.basename(script_path)[:-3]
            target.append((script_name, script_path))
    
    def execute_init(self):
        sys.path.append(f"{self.path}/py_path/")
    
    def execute_early(self, datapack, moddata):
        # Execute any early scripts in the module
        for script in self.py_init_scripts:
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
        for script in self.js_common_scripts:
            script_name, script_path = script
            print(f"  - Copying '{script_path}'")
            datapack._kubejs_copy_script(f"client_scripts/{self.module_name}-{script_name}", ".js", script_path)
            datapack._kubejs_copy_script(f"server_scripts/{self.module_name}-{script_name}", ".js", script_path)
            datapack._kubejs_copy_script(f"startup_scripts/{self.module_name}-{script_name}", ".js", script_path)
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
                    data = json.dumps(json5.loads(open(file_path).read()), indent=True)
                    datapack._write_data(short_path, kind, data)
                else:
                    datapack._copy_data(short_path, kind, file_path)
    
    def _copy_scripts_js(self, datapack, target, kind):
        for script in target:
            script_name, script_path = script
            print(f"  - Copying '{script_path}'")
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

    def execute_init(self):
        for module in self.modules:
            module.execute_init()
    def execute_early(self, datapack, moddata):
        for module in self.modules:
            module.execute_early(datapack, moddata)
    def execute_late(self, datapack, moddata):
        for module in self.modules:
            module.execute_late(datapack, moddata)
    def execute(self, datapack, moddata):
        for module in self.modules:
            module.execute(datapack, moddata)
