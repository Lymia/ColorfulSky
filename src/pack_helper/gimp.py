import math
import os
import os.path
import multiprocessing
import secrets
import shutil
import subprocess
import time

from pack_helper.utils import *

def reset(run_path):
    shutil.rmtree(f"{run_path}/gimp", ignore_errors=True)

def _join_ln(l):
    if len(l) == 0:
        return ""
    else:
        return "\n"+"\n".join(l)+"\n"
def _join(l):
    if len(l) == 0:
        return ""
    else:
        return "\n"+"".join(l)
def _str(s):
    if s == None:
        return "nil"
    else:
        return repr(s).replace("'", '"')
def _null(v):
    if v == None:
        return "nil"
    else:
        return v

class GimpAstElement(object):
    def __init__(self, elem_name, elem_code, *parents):
        self._elem_name = f"{elem_name}-{secrets.token_hex(8)}"
        self._elem_code = elem_code
        self._parents = list(parents)
        self._bind = True
    def _serialize(self):
        return self._elem_code
        
class GimpImageElement(GimpAstElement):
    def __init__(self, elem_name, elem_code):
        super().__init__(elem_name, elem_code)
        self._img_name = self._elem_name
        
    def load_xcf(path):
        path_str = repr(path).replace("'", '"')
        return GimpImageElement("xcf_image", f"(cs-load-xcf {path_str})")
    def load_png(path):
        path_str = repr(path).replace("'", '"')
        return GimpImageElement("png_image", f"(cs-load-png {path_str})")
    
    def mutable_scope(self):
        return GimpImageMutableScope("xcf_mutable_scope", self._elem_name, self)
        
class GimpImageMutableScope(GimpAstElement):
    def __init__(self, elem_name, elem_code, parent_elem):
        super().__init__(elem_name, elem_code, parent_elem)
        self._bind = False
        self._parent_elem = parent_elem._elem_name
        self._commands = []
        self._commands_tail = []
        self._img_name = self._elem_name
    def _serialize(self):
        return f"(let (({self._elem_name} {self._parent_elem})){_join_ln(self._commands)}{_join(self._commands_tail)})"
    
    def get_layer_by_name(self, name):
        layer_name = f"layer-{secrets.token_hex(8)}"
        self._commands.append(f"(let (({layer_name} (cs-maybe-layer-by-name {self._elem_name} {_str(name)})))")
        self._commands_tail.append(")")
        return layer_name

    def new_layer(self, parent = None):
        layer_name = f"new-layer-{secrets.token_hex(8)}"
        self._commands.append(f"(let (({layer_name} (cs-new-layer {self._elem_name} {_str(layer_name)})))")
        if parent != None:
            self.attach_to_group(parent, layer_name)
        self._commands_tail.append(")")
        return layer_name
    def delete_layer(self, layer):
        self._commands.append(f"(gimp-image-remove-layer {self._elem_name} {layer})")
    def attach_to_group(self, parent, child):
        self._commands.append(f"(cs-append-layer {self._elem_name} {parent} {child})")
    def copy_image_to_layer(self, layer, image, source_layer = None):
        self._commands.append(f"(cs-transfer-image-to-layer {image._elem_name} {_str(source_layer)} {layer})")
        self._parents.append(image)
    def save_png(self, path, layer = None):
        self._commands.append(f"(cs-png-save {self._elem_name} {_null(layer)} {_str(path)})")
        
def _resolve_tree(actions):
    action_list = []
    seen = set({})
    def recurse(action):
        if not id(action) in seen:
            action_list.append(action)
            seen.add(id(action))
            for parent in action._parents:
                recurse(parent)
    for action in actions:
        recurse(action)
        
    accum_head = ""
    accum_tail = ""
    resolved = set({})
    while len(action_list) != 0:
        new_actions = []
        new_vars = []
        new_commands = []
        new_resolved = []
        
        for action in action_list:
            if all(map(lambda x: x._elem_name in resolved, action._parents)):
                new_resolved.append(action._elem_name)
                if action._bind:
                    new_vars.append(f"({action._elem_name} {action._serialize()})")
                else:
                    new_commands.append(action._serialize())
            else:
                new_actions.append(action)
                
        if len(new_commands) != 0:
            accum_tail = f"{_join_ln(new_commands)}{accum_tail}"
        if len(new_vars) != 0:
            accum_head = f"{accum_head}\n(let ({_join_ln(new_vars)})\n"
            accum_tail = f"{accum_tail}\n)"

        action_list = new_actions
        for name in new_resolved:
            resolved.add(name)
        
    return f"(begin\n{accum_head}{accum_tail}\n)"

class GimpContext(object):
    def __init__(self, run_path):
        self._run_path = run_path
        
        # Create temporary directories
        self._scripts_path = f"{run_path}/gimp/scripts_{secrets.token_hex(8)}"
        os.makedirs(self._scripts_path, exist_ok = True)
        
        # Create gimprc
        self._gimprc_path = f"{run_path}/gimp/config_{secrets.token_hex(8)}.gimprc"
        static_scripts = f"{os.path.dirname(__file__)}/gimp_scripts"
        with open_mkdir(self._gimprc_path) as fd:
            fd.write(f"""
                (script-fu-path "{self._scripts_path}:{static_scripts}:${{gimp_data_dir}}/scripts")
                (restore-session no)
                (save-session-info no)
                (trust-dirty-flag no)
                (save-document-history no)
                (undo-levels 0)
            """)
    
    def _run_script(self, script_code):
        script_path = f"{self._scripts_path}/script_{secrets.token_hex(8)}.scm"
        function_name = f"run-script-{secrets.token_hex(8)}"
        
        script_data = f"(define ({function_name})\n{script_code}\n)"
        with open_mkdir(script_path) as fd:
            fd.write(script_data)

        return subprocess.Popen([
            shutil.which("gimp"), 
            "--console-messages", f"--gimprc={self._gimprc_path}", "-idf", "-b", 
            f"({function_name})", "-b", "(gimp-quit 0)"
        ])
        
    def execute_actions(self, actions, max_processes = multiprocessing.cpu_count(), process_chunk = None):
        if process_chunk == None:
            process_chunk = max(math.ceil(len(actions) / max_processes), 4)
        
        processes = []
        while len(actions) != 0:
            cur_actions = actions[:process_chunk]
            actions = actions[process_chunk:]
            
            processes.append(self._run_script(_resolve_tree(cur_actions)))
            while len(processes) > max_processes:
                processes = list(filter(lambda x: x.poll() == None, processes))
                time.sleep(1.0)
                
        for process in processes:
            process.wait()
