import glob
import importlib.util
import os.path
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
        
        self.js_common_scripts = []
        self.js_client_scripts = []
        self.js_server_scripts = []
        self.js_startup_scripts = []
        
        # Load Python scripts
        self._load_scripts_py(self.py_scripts, "py_scripts")
        self._load_scripts_py(self.py_init_scripts, "py_init_scripts")
            
        # Load KubeJS scripts
        self._load_scripts_js(self.js_common_scripts, "common_scripts")
        self._load_scripts_js(self.js_client_scripts, "client_scripts")
        self._load_scripts_js(self.js_server_scripts, "server_scripts")
        self._load_scripts_js(self.js_startup_scripts, "startup_scripts")
        for script_path in glob.glob(f"{path}/common_scripts/*.js"):
            script_name = os.path.basename(script_path)[:-3]
            self.js_common_scripts.append((script_name, script_path))
            
        # TODO: Load other resources.
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
    def execute_early(self):
        # Execute any early scripts in the module
        for script in self.py_init_scripts:
            script.execute(datapack, moddata)
    def execute(self, datapack, moddata):
        # Execute any scripts in the module
        for script in self.py_scripts:
            print(f"  - Running '{script.script_file}'...")
            script.execute(datapack, moddata)
        
        # Copy Javascript scripts
        self._copy_scripts_js(datapack, self.js_common_scripts, "common_scripts")
        self._copy_scripts_js(datapack, self.js_client_scripts, "client_scripts")
        self._copy_scripts_js(datapack, self.js_server_scripts, "server_scripts")
        self._copy_scripts_js(datapack, self.js_startup_scripts, "startup_scripts")
    def _copy_scripts_js(self, datapack, target, kind):
        for script in target:
            script_name, script_path = script
            print(f"  - Copying '{script_path}'")
            datapack._kubejs_copy_script(f"{kind}/{self.module_name}-{script_name}", ".js", script_path)

class ModuleLoader(object):
    modules = []
    
    def __init__(self):
        self.modules.append(Module(f"{os.path.dirname(__file__)}/BaseModule"))
        for script_path in glob.glob(f"modules/*"):
            self.modules.append(Module(script_path))
    
    def execute_init(self):
        for module in self.modules:
            module.execute_init()
    def execute_early(self):
        for module in self.modules:
            module.execute_early()
    def execute(self, datapack, moddata):
        for module in self.modules:
            module.execute(datapack, moddata)
