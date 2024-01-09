from pack_helper.utils import *

remove_items_list = [
    # Cyclic
    # TODO: Remove entires for these from the book.
    "cyclic:disenchanter", # Causes exploit with Silent's Gear/Silent's Gems.
    "cyclic:uncrafter", # Causes exploits with literally everything.
    "cyclic:heart", # Mathematically dangerous with Minecraft armor.
    "cyclic:tile_transporter_empty", # This is just *asking* for trouble.
    
    # ProjectE
    "projecte:collector_mk1", # In an extensive modpack, collectors are unnessecary. Just burn stuff outta a farm.
    "projecte:collector_mk2",
    "projecte:collector_mk3",
    "projecte:rm_katar", # kinda excessive fusion items
    "projecte:rm_morning_star",
    "projecte:dm_helmet", # ProjectE armors are very powerful, and kinda invalidate everything else.
    "projecte:dm_chestplate",
    "projecte:dm_leggings",
    "projecte:dm_boots",
    "projecte:rm_helmet",
    "projecte:rm_chestplate",
    "projecte:rm_leggings",
    "projecte:rm_boots",
    "projecte:gem_helmet",
    "projecte:gem_chestplate",
    "projecte:gem_leggings",
    "projecte:gem_boots",
    "projecte:archangel_smite", # Ridicilous weapon
    "projecte:swiftwolf_rending_gale", # Offensive ability too powerful    
    "projecte:arcana_ring", # Components of ring already removed
    "projecte:life_stone", # The soul stone is already sliiightly powerful on its own
    "projecte:hyperkinetic_lens", # Power level is just excessive by any standard
    "projecte:catalytic_lens",
    "projecte:nova_cataclysm", # big boom :(
    
    # Remove Bort
    "silentgear:bort",
    "silentgear:bort_block",
    
    # Remove Quark Brimstone
    "quark:brimstone",
    "quark:brimstone_slab",
    "quark:brimstone_stairs",
    "quark:brimstone_wall",
    "quark:brimstone_bricks",
    "quark:brimstone_bricks_slab",
    "quark:brimstone_bricks_stairs",
    "quark:brimstone_bricks_wall",
    "quark:brimstone_vertical_slab",
    "quark:brimstone_bricks_vertical_slab",
    
    # Useless documentation
    "valkyrielib:info_tablet",
    "theoneprobe:probenote",
    "silentgear:guide_book",
]
change_i18n = [
    # Conflict with BYG Brimstone
    ("betterendforge:brimstone", "Hydrothermal Brimstone"),
]

for item in remove_items_list:
    datapack.remove_name(item)
for entry in change_i18n:
    item, name = entry
    datapack.add_i18n(group(item), f"block.{group(item)}.{path(item)}", name)
