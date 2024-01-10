#!/usr/bin/env python3

import toml

missing_materials = [
    "cloggrum", "ender", "froststeel", "nebu", "pink_slime", "aluminum", "iridium", "agate", "amber",
    "benitoite", "biotite", "cats_eye", "charged_certus_quartz", "chrysoprase", "euclase", "garnet",
    "green_sapphire", "jade", "jasper", "kunzite", "lepidolite", "malachite", "moonstone", "morganite",
    "onyx", "opal", "pearl", "phosphophyllite", "pyrope", "rose_quartz", "sodalite", "spinel",
    "sunstone", "tanzanite", "tektite", "yellow_diamond", "zircon", "coral", "bort", "certus_quartz",
]
target_modules = [
    "storage_blocks", "colorfulsky_raw_ore", "colorfulsky:raw_ore", "dusts", "molten", "ingot",
    "mekanism", "mekanism_clean", "mekanism_dirty",
]

for mat in missing_materials:
    data = {
        "general": {
            "alternativeNames": [],
            "extras": [],
            "isSmallStorageBlock": False,
            "moduleBlacklist": target_modules,
            "hasEffect": False,
            "modelType": "metallic",
            "color": 0xFF00FF,
        },
    }
    open(f"{mat}.toml", "w").write(toml.dumps(data))
