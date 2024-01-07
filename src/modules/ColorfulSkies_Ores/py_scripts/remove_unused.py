unused_ores = [
    # Replaced
    "silentgems:ender_ore",
    "betterendforge:ender_ore",
    
    # Not used due to the silent's gems rework
    "silentgems:multi_ore_classic",
    "silentgems:multi_ore_dark",
    "silentgems:multi_ore_light",
    
    # Remove Bort
    "silentgear:bort",
    "silentgear:bort_block",
    
    # Mystical Agriculture
    "projecte:prosperity_ore", # We use a recipe instead of an ore for this.
    "projecte:inferium_ore", # We just let mob drops cover this.    
    
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
    
    # Remove Anthracite
    "byg:anthracite",
    "byg:anthracite_block",
    
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
    "minecraft:nether_gold_ore",
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
]

for unused in unused_ores:
    datapack.remove_name(unused)
