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
    py_scripts = []
    py_init_scripts = []
    
    def __init__(self, path):
        if path[-1] == "/":
            path = path[:-1]
        self.module_name = os.path.basename(path)
        self.path = path
        
        # Load Python scripts
        for script_path in glob.glob(f"{path}/py_scripts/*.py"):
            script_name = os.path.basename(script_path)[:-3]
            self.py_scripts.append(Script(self, f"modules.{self.module_name}.{script_name}", script_path))
        for script_path in glob.glob(f"{path}/py_init_scripts/*.py"):
            script_name = os.path.basename(script_path)[:-3]
            self.py_init_scripts.append(Script(self, f"modules.{self.module_name}.{script_name}", script_path))
            
        # TODO: Load other resources.
    
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

class ModuleLoader(object):
    modules = []
    
    def __init__(self):
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
