import os
import json
import shutil
import zipfile

from pack_helper.ctx import *
from pack_helper.utils import *

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

target = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
zip_file = zipfile.ZipFile(find_pack("DP+Pack"))
exists = set(zip_file.namelist())

for model in moddata.glob("assets/draconicevolution/models/**/*.json"):
    target_path = f"{target}/{model}"
    changed = False
    model = json.loads(moddata.read_path(model))
    if "textures" in model:
        for texture in model["textures"]:
            resource = model["textures"][texture]
            if not f"assets/{dir_for_texture(resource)}" in exists:
                for replacement in replacements:
                    mapped = resource.replace(replacement[0], replacement[1])
                    if f"assets/{dir_for_texture(mapped)}" in exists:
                        resource = mapped
                        changed = True
                        break
            model["textures"][texture] = resource
    if changed:
        os.makedirs(os.path.dirname(target_path), exist_ok = True)
        with open(target_path, "w") as fd:
            fd.write(json.dumps(model))
