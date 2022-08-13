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
    
    # Mystical Agriculture
    "projecte:prosperity_ore", # We use a recipe instead of an ore for this.
    "projecte:inferium_ore", # We just let mob drops cover this.
    
    # Redundant ores
    "ars_nouveau:arcane_ore",
    "create:copper_ore",
    "create:zinc_ore",
    "darkerdepths:silver_ore",
    "draconicevolution:end_draconium_ore",
    "draconicevolution:nether_draconium_ore",
    "draconicevolution:overworld_draconium_ore",
    "eidolon:lead_ore",
    "immersiveengineering:ore_copper",
    "immersiveengineering:ore_lead",
    "immersiveengineering:ore_silver",
    "immersiveengineering:ore_nickel",
    "immersiveengineering:ore_uranium",
    "mekanism:copper_ore",
    "mekanism:tin_ore",
    "mekanism:osmium_ore",
    "mekanism:uranium_ore",
    "mekanism:fluorite_ore",
    "mekanism:lead_ore",
    "rftoolsbase:dimensionalshard_overworld",
    "rftoolsbase:dimensionalshard_nether",
    "rftoolsbase:dimensionalshard_end",
    "silentgear:bort_ore",
    "silentgear:deepslate_bort_ore",
    "silentgems:silver_ore",
    "tconstruct:copper_ore",
    "thermal:nickel_ore",
    "thermal:silver_ore",
    "thermal:lead_ore",
    "thermal:tin_ore",
    "thermal:copper_ore",
    "thermal:sulfur_ore",
    "thermal:niter_ore",
    "thermal:cinnabar_ore",
    "tmechworks:aluminum_ore",
    "tmechworks:copper_ore",
    
    # Remove Bort
    "silentgear:bort",
    "silentgear:bort_block",
    
    # Remove aluminium
    "immersiveengineering:sheetmetal_aluminum",
    "immersiveengineering:slab_sheetmetal_aluminum",
    "immersiveengineering:ore_aluminum",
    "immersiveengineering:storage_aluminum",
    "immersiveengineering:slab_storage_aluminum",
    "chisel:metals/aluminum/caution",
    "chisel:metals/aluminum/crate",
    "chisel:metals/aluminum/thermal",
    "chisel:metals/aluminum/machine",
    "chisel:metals/aluminum/badgreggy",
    "chisel:metals/aluminum/bolted",
    "chisel:metals/aluminum/scaffold",
    "immersiveengineering:plate_aluminum",
    "immersiveengineering:dust_aluminum",
    "immersiveengineering:nugget_aluminum",
    "immersiveengineering:ingot_aluminum",
    "immersiveengineering:stick_aluminum",
    "immersiveengineering:wire_aluminum",
    "tmechworks:aluminum_block",
    "tmechworks:aluminum_ingot",
    "tmechworks:aluminum_nugget",
    
    # Remove ender biotite
    "quark:biotite_ore",
    "quark:biotite_block",
    "quark:biotite_block_slab",
    "quark:biotite_block_stairs",
    "quark:smooth_biotite",
    "quark:smooth_biotite_slab",
    "quark:smooth_biotite_stairs",
    "quark:chiseled_biotite_block",
    "quark:biotite_pillar",
    "quark:biotite_bricks",
    "quark:biotite_block_vertical_slab",
    "quark:smooth_biotite_vertical_slab",
    "quark:biotite",
]

def add_fixes(data):
    for item in remove_items_list:
        data.remove_name(item)
