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
    (":block/", ":blocks/animated/"),
    (":block/", ":models/"),
    (":item/", ":models/"),
    
    # Draconic Evolution
    (":item/advanced_dislocator", ":items/dislocator_advanced"),
    (":item/un_bound_dislocator", ":items/dislocator"),
    (":item/bound_dislocator", ":items/dislocator_bound"),
    (":item/advanced_magnet", ":items/magnet_advanced"),
    (":item/magnet", ":items/magnet_basic"),
    
    (":item/components/awakened_draconium_ingot", ":items/components/draconic_ingot"),
    (":item/components/awakened_draconium_nugget", ":items/components/nugget_awakened"),
    (":item/components/draconium_core", ":items/components/draconic_core"),
    (":item/components/draconium_nugget", ":items/components/nugget_draconium"),
    
    (":item/tools/draconic_capacitor", ":items/capacitors/draconic_capacitor"),
    (":item/tools/wyvern_capacitor", ":items/capacitors/wyvern_capacitor"),
    (":item/tools/creative_capacitor", ":items/capacitors/creative_capacitor"),
    
    (":block/awakened_draconium_block", ":blocks/draconium_block_charged"),
    (":block/awakened_draconium_block_side", ":blocks/draconium_block_charged"),
    (":block/creative_op_capacitor", ":blocks/animated/creative_rf_source"),
    (":block/dislocation_inhibitor", ":blocks/item_dislocation_inhibitor_side"),
    (":block/end_draconium_ore", ":blocks/animated/draconium_ore_end"),
    (":block/energy_core", ":blocks/animated/energy_storage_core"),
    (":block/energy_core_stabilizer", ":blocks/particle_gen/stabilizer"),
    # What is the energy tranfuser? New?
    # Grinder needs revision.
    (":block/nether_draconium_ore", ":blocks/animated/draconium_ore_nether"),
    (":block/overworld_draconium_ore", ":blocks/animated/draconium_ore_overworld"),
    (":block/particle_generator", ":blocks/animated/particle_gen/normal"),
    (":block/stabilzer_large", ":blocks/particle_gen/stabilizer_large"),
    
    (":block/core/", ":models/"),
    (":block/core/stabilizer_sphere", ":blocks/obj_textures/stabilizer_sphere"),
    
    (":block/crafting/", ":blocks/fusion_crafting"),
    
    (":block/reactor/", ":models/"),
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
