import glob
import os
import os.path
import json
import shutil

from gen.utils import *

exclude = [
    "projecte:",
]
replacements = [
    # Generic
    (":item/", ":items/"),
    (":block/", ":blocks/"),
    # Draconic Evolution
]

def generate_model_fixes(resource_pack, mod, target):
    for model in glob.glob(f"{mod}/assets/*/models/**/*.json"):
        target_path = f"{target}{model[len(mod):]}"
        changed = False
        with open(model) as fd:
            model = json.loads(fd.read())
        if "textures" in model:
            for texture in model["textures"]:
                resource = model["textures"][texture]
                
                excluded = False
                for prefix in exclude:
                    if resource.startswith(prefix):
                        excluded = True
                if excluded:
                    continue
                if not os.path.exists(f"{resource_pack}/assets/{dir_for_texture(resource)}"):
                    for replacement in replacements:
                        mapped = resource.replace(replacement[0], replacement[1])
                        if os.path.exists(f"{resource_pack}/assets/{dir_for_texture(mapped)}"):
                            resource = mapped
                            changed = True
                            break
                
                model["textures"][texture] = resource
        if changed:
            os.makedirs(os.path.dirname(target_path), exist_ok = True)
            with open(target_path, "w") as fd:
                fd.write(json.dumps(model))
