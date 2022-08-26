import json
import types

from pack_helper.utils import *

# TODO: Sided blocks (Grimestone, Blackstone, Brimstone, Basalt, Scoria, Ether Stone, Deepslate)
# TODO: Darker Depths unneeded definitions
# TODO: Figure out how to unscrew Alfheim

# TODO: Add manual ore textures for a few particularly problematic combinations

twilight_forest_biomes = [
    "twilightforest:clearing",
    "twilightforest:dark_forest_center",
    "twilightforest:dark_forest",
    "twilightforest:dense_forest",
    "twilightforest:dense_mushroom_forest",
    "twilightforest:enchanted_forest",
    "twilightforest:final_plateau",
    "twilightforest:firefly_forest",
    "twilightforest:fire_swamp",
    "twilightforest:forest",
    "twilightforest:glacier",
    "twilightforest:highlands",
    "twilightforest:lake",
    "twilightforest:mushroom_forest",
    "twilightforest:oak_savannah",
    "twilightforest:snowy_forest",
    "twilightforest:spooky_forest",
    "twilightforest:stream",
    "twilightforest:swamp",
    "twilightforest:thornlands",
]

###################################
# Ore Type and Strata definitions #
###################################

ore_types = {}
ore_stratas = {}

def add_type(name, display_name, strength, resistance, harvest_level, kind, *categories, 
             drop_loot_table=None, drop_name=None, cluster_name=None, min_count=1, max_count=1,
             is_custom=False, disabled=False):
    record = types.SimpleNamespace()
    record.name = name
    record.display_name = display_name
    record.custom = is_custom
    record.disabled = disabled
    record.strength = strength
    record.resistance = resistance
    record.harvest_level = harvest_level
    record.kind = kind
    record.categories = categories
    record.worldgen = {}
    record.overrides = {}
    record.keep_texture = {}
    record.no_generation = set({})
    record.spawn_modifier = {}
    record.drop_loot_table = drop_loot_table
    record.drop_name = drop_name
    record.cluster_name = cluster_name
    record.min_count = min_count
    record.max_count = max_count
    ore_types[record.name] = record
def add_worldgen(name, cluster_size, cluster_count, height_range, target="default"):
    record = types.SimpleNamespace()
    record.cluster_size = cluster_size
    record.cluster_count = cluster_count
    record.min_y = height_range[0]
    record.max_y = height_range[1]
    ore_types[name].worldgen[target] = record
def add_ore_override(name, strata, block, keep_texture=False):
    ore_types[name].overrides[strata] = block
    if keep_texture:
        ore_types[name].keep_texture[strata] = True
def add_unneeded(name, strata):
    ore_types[name].no_generation.add(strata)

def add_strata(name, display_name, texture, parent_stone, *categories, 
               is_custom=False, disabled=False, material="stone", harvest_tool="pickaxe"):
    record = types.SimpleNamespace()
    record.name = name
    record.display_name = display_name
    record.custom = is_custom
    record.disabled = disabled
    if is_custom:
        record.ee_suffix = None
    elif name == "stone":
        record.ee_suffix = ""
    else:
        record.ee_suffix = f"_{name}"
    record.texture = texture
    record.parent_stone = parent_stone
    record.categories = categories
    record.material = material
    record.harvest_tool = harvest_tool
    ore_stratas[record.name] = record

# Built-in ore types
add_type("coal", "Coal", 3, 3, 0, "gem", "overworld", "twilight",
         drop_name="minecraft:coal")
add_type("iron", "Iron", 3, 3, 1, "ingot", "overworld", "twilight",
         min_count=1, max_count=2)
add_type("gold", "Gold", 3, 3, 2, "ingot", "overworld", "nether")
add_type("diamond", "Diamond", 3, 3, 2, "gem", "overworld", "twilight",
         drop_name="minecraft:diamond")
add_type("emerald", "Emerald", 3, 3, 2, "gem", "end",
         drop_name="minecraft:emerald")
add_type("lapis", "Lapis", 3, 3, 1, "gem", "overworld", "nether",
         drop_name="minecraft:lapis_lazuli", min_count=4, max_count=9)
add_type("redstone", "Redstone", 3, 3, 2, "gem", "overworld",
         drop_name="minecraft:redstone", min_count=4, max_count=5)
add_type("quartz", "Quartz", 3, 3, 2, "gem", "nether",
         drop_name="minecraft:quartz")
add_type("copper", "Copper", 3, 3, 1, "ingot", "overworld",
         min_count=2, max_count=3)
add_type("silver", "Silver", 3, 3, 2, "ingot", "twilight", "end")
add_type("lead", "Lead", 3, 3, 2, "ingot", "twilight")
add_type("nickel", "Nickel", 3, 3, 2, "ingot", "twilight")
add_type("uranium", "Uranium", 3, 3, 2, "ingot", "nether")
add_type("osmium", "Osmium", 3, 3, 1, "ingot", "twilight", "end")
add_type("zinc", "Zinc", 3, 3, 2, "ingot", "overworld", "end")
add_type("fluorite", "Fluorite", 3, 3, 1, "gem", "end",
         drop_name="emendatusenigmatica:fluorite_gem", min_count=2, max_count=4)
add_type("sulfur", "Sulfur", 3, 3, 1, "gem", "nether",
         drop_name="emendatusenigmatica:sulfur_gem", min_count=3, max_count=5)
add_type("arcane", "Source Gem", 3, 3, 1, "gem", "twilight", "end",
         drop_name="emendatusenigmatica:arcane_gem")
add_type("dimensional", "Dimensional Shard", 3, 3, 1, "gem", "twilight", "nether", "end",
         drop_name="emendatusenigmatica:dimensional_gem", min_count=4, max_count=5)
add_type("cobalt", "Cobalt", 3, 3, 2, "ingot", "nether")
add_type("tin", "Tin", 3, 3, 1, "ingot", "overworld")

# TODO: Crimson Iron
# TODO: Geode
# TODO: Thallasium
# TODO: Azure Silver
# TODO: Rock Crystal (maybe?)

# Unused ore types
add_type("aluminum", "Aluminum", 3, 3, 1, "ingot", "overworld", "twilight", "end", disabled = True)
add_type("apatite", "Apatite", 3, 3, 1, "gem", "overworld",
         drop_name="emendatusenigmatica:apatite_gem", min_count=4, max_count=9,
         disabled = True)
add_type("bitumen", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("cinnabar", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("certus_quartz", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("charged_certus_quartz", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("iridium", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("peridot", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("potassium_nitrate", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("ruby", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("sapphire", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems

# EE built-in strata
add_strata("stone", "Stone", "minecraft:block/stone", "minecraft:stone", "overworld", "twilight")
add_strata("andesite", "Andesite", "minecraft:block/andesite",  "minecraft:andesite", "overworld")
add_strata("granite", "Granite", "minecraft:block/granite",  "minecraft:granite", "overworld")
add_strata("diorite", "Diorite", "minecraft:block/diorite",  "minecraft:diorite", "overworld")
add_strata("sand", "Sand", None, None, "overworld", disabled=True)
add_strata("gravel", "Gravel", None, None, "overworld", disabled=True)
add_strata("netherrack", "Netherrack", "minecraft:block/netherrack",  "minecraft:netherrack", "nether")
add_strata("blackstone", "Blackstone", "minecraft:block/blackstone",  "minecraft:blackstone", "nether") # TODO: Sided.
add_strata("basalt", "Basalt", "minecraft:block/basalt_side",  "minecraft:basalt", "nether") # TODO: Sided
add_strata("end_stone", "End Stone", "minecraft:block/end_stone",  "minecraft:end_stone", "end")
add_strata("soul_soil", "Soul Soil", "minecraft:block/soul_soil",  "minecraft:soul_soil", "nether", disabled=True)

add_strata("gabbro", "Gabbro", "create:block/palettes/gabbro/plain", "create:gabbro", "overworld", "twilight")
add_strata("c_limestone", "Limestone", "create:block/palettes/limestone/plain", "create:limestone", "overworld", disabled=True),
add_strata("scoria", "Scoria", "create:block/palettes/natural_scoria", "create:natural_scoria", "overworld", "twilight"),
add_strata("weathered_limestone", "Weathered Limestone", "create:block/palettes/weathered_limestone/plain", "create:weathered_limestone", "overworld", "twilight"),

add_strata("jasper", "Jasper", "quark:block/jasper", "quark:jasper", "overworld")
add_strata("marble", "Marble", "quark:block/marble", "quark:marble", "overworld")
add_strata("slate", "Slate", "quark:block/slate", "quark:slate", "overworld")
add_strata("deepslate", "Deepslate", "quark:block/backport/deepslate", "quark:deepslate", "overworld")

add_strata("mossy_stone", "Mossy Stone", "byg:block/mossy_stone", "byg:mossy_stone", "overworld")
add_strata("subzero_ash", "Subzero Ash", "byg:block/subzero_ash", "byg:subzero_ash_block", "nether", disabled=True)
add_strata("blue_netherrack", "Blue Netherrack", "byg:block/blue_netherrack", "byg:blue_netherrack", "nether")
add_strata("nylium_soul_soil", "Nylium Soul Soil", "byg:block/nylium_soul_soil", "byg:nylium_soul_soil", "nether", disabled=True)
add_strata("brimstone", "Brimstone", "byg:block/brimstone", "byg:brimstone", "nether")

add_strata("cryptic_stone", "Cryptic Stone", "byg:block/cryptic_stone", "byg:cryptic_stone", "end")
add_strata("flavolite", "Flavolite", "betterendforge:block/flavolite", "betterendforge:flavolite", "end")
add_strata("sulphuric_rock", "Sulphuric Rock", "betterendforge:block/sulphuric_rock", "betterendforge:sulphuric_rock", "end")
add_strata("violecite", "Violecite", "betterendforge:block/violecite", "betterendforge:violecite", "end")
add_strata("ether_stone", "Ether Stone", "byg:block/ether_stone", "byg:ether_stone", "end")

add_strata("raw_marble", "Marble", "astralsorcery:block/marble_raw", "astralsorcery:marble_raw", "overworld", disabled=True)

# Custom strata
add_strata("clay", "Clay", "minecraft:block/clay", "minecraft:clay", "overworld", is_custom=True, material="clay", harvest_tool="shovel")
add_strata("dolomite", "Dolomite", "create:block/palettes/dolomite/plain", "create:dolomite", "overworld", "twilight", is_custom=True)
add_strata("aridrock", "Aridrock", "darkerdepths:block/aridrock", "darkerdepths:aridrock", "overworld", is_custom=True)
add_strata("grimestone", "Grimestone", "darkerdepths:block/grimestone", "darkerdepths:grimestone", "overworld", is_custom=True) # TODO: Sided
add_strata("dd_limestone", "Limestone", "darkerdepths:block/limestone", "darkerdepths:limestone", "overworld", is_custom=True)
add_strata("dacite", "Dacite", "byg:block/dacite", "byg:dacite", "overworld", is_custom=True)
add_strata("red_rock", "Red Rock", "byg:block/red_rock", "byg:red_rock", "overworld", is_custom=True)
add_strata("soapstone", "Soapstone", "byg:block/soapstone", "byg:soapstone", "overworld", is_custom=True)
add_strata("q_limestone", "Limestone", "quark:block/limestone", "quark:limestone", "overworld", is_custom=True)
add_strata("shale", "Shale", "darkerdepths:block/shale", "darkerdepths:shale", "overworld", is_custom=True)
add_strata("umbralith", "Umbralith", "betterendforge:block/umbralith", "betterendforge:umbralith", "end", is_custom=True)

add_strata("travertine", "Travertine", "byg:block/travertine", "byg:travertine", "nether", is_custom=True)
add_strata("quartzite", "Quartzite", "byg:block/quartzite_sand", "byg:quartzite_sand", "nether", is_custom=True, material="sand", harvest_tool="shovel")
add_strata("scoria_stone", "Scoria Stone", "byg:block/scoria_stone", "byg:scoria_stone", "nether", is_custom=True),
add_strata("s_soul_soil", "Soul Soil", "minecraft:block/soul_soil",  "minecraft:soul_soil", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("s_nylium_soul_soil", "Nylium Soul Soil", "byg:block/nylium_soul_soil", "byg:nylium_soul_soil", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("s_subzero_ash", "Subzero Ash", "byg:block/subzero_ash", "byg:subzero_ash_block", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("dullstone", "Dullstone", "infernalexp:block/dullstone", "infernalexp:dullstone", "nether", is_custom=True),
add_strata("shimmerstone", "Shimmerstone", "infernalexp:block/glowdust_stone", "infernalexp:glowdust_stone", "nether", is_custom=True),

# Ore overrides
for ore in ["coal", "iron", "gold", "diamond", "redstone", "lapis", "emerald"]:
    add_ore_override(ore, "stone", f"minecraft:{ore}_ore", keep_texture = True)
    add_ore_override(ore, "deepslate", f"cavesandcliffs:deepslate_{ore}_ore", keep_texture = True)
add_ore_override("copper", "stone", "cavesandcliffs:copper_ore", keep_texture = True)
add_ore_override("copper", "deepslate", "cavesandcliffs:deepslate_copper_ore", keep_texture = True)
add_ore_override("quartz", "netherrack", "minecraft:nether_quartz_ore", keep_texture = True)
for ore in ["gold", "iron", "coal", "lapis", "diamond", "redstone", "silver"]:
    add_ore_override(ore, "dd_limestone", f"darkerdepths:limestone_{ore}_ore")
    add_ore_override(ore, "aridrock", f"darkerdepths:aridrock_{ore}_ore")

# Unneeded ores
add_unneeded("quartz", "quartzite")
add_unneeded("coal", "brimstone") # Lignite
add_unneeded("coal", "ether_stone") # Anthracite

####################
# Worldgen configs #
####################

add_worldgen('coal', 13, 21, (10, 100), target = 'overworld')
add_worldgen('iron', 11, 13, (10, 64), target = 'overworld')
add_worldgen('copper', 7, 13, (15, 60), target = 'overworld')
add_worldgen('gold', 8, 9, (10, 30), target = 'overworld')
add_worldgen('redstone', 11, 8, (5, 25), target = 'overworld')
add_worldgen('tin', 7, 11, (20, 40), target = 'overworld')
add_worldgen('zinc', 7, 11, (30, 50), target = 'overworld')
add_worldgen('lapis', 7, 5, (0, 20), target = 'overworld')
add_worldgen('diamond', 9, 3, (0, 16), target = 'overworld')
# TODO: Geode

add_worldgen('quartz', 17, 21, (20, 128), target = 'nether')
add_worldgen('gold', 13, 17, (20, 128), target = 'nether')
add_worldgen('sulfur', 13, 13, (20, 128), target = 'nether')
add_worldgen('lapis', 13, 9, (10, 60), target = 'nether')
add_worldgen('cobalt', 8, 6, (40, 80), target = 'nether')
# TODO: Crimson Iron
add_worldgen('uranium', 8, 5, (25, 45), target = 'nether')
# TODO: Geode
add_worldgen('dimensional', 3, 5, (10, 60), target = 'nether')

# TODO: Thallasium
# TODO: Azure Silver
add_worldgen('osmium', 13, 21, (10, 90), target = 'end')
add_worldgen('zinc', 8, 17, (10, 90), target = 'end')
add_worldgen('arcane', 6, 11, (10, 90), target = 'end')
add_worldgen('silver', 13, 21, (10, 90), target = 'end')
add_worldgen('fluorite', 8, 11, (10, 90), target = 'end')
# TODO: Geode
add_worldgen('dimensional', 3, 7, (10, 60), target = 'end')
add_worldgen('emerald', 3, 7, (10, 60), target = 'end')

add_worldgen('coal', 13, 17, (0, 64), target = 'twilight')
add_worldgen('iron', 11, 11, (0, 40), target = 'twilight')
add_worldgen('nickel', 8, 9, (15, 30), target = 'twilight')
add_worldgen('lead', 8, 9, (0, 15), target = 'twilight')
add_worldgen('osmium', 8, 9, (10, 20), target = 'twilight')
add_worldgen('arcane', 6, 6, (0, 25), target = 'twilight')
add_worldgen('diamond', 8, 3, (0, 15), target = 'twilight')
add_worldgen('silver', 8, 7, (10, 35), target = 'twilight')
# TODO: Geode
add_worldgen('dimensional', 3, 5, (0, 16), target = 'twilight')

###########################
# Ore list generator code #
###########################

def name_for_ore(otype, strata):
    return f"{otype.name}_{strata.name}_ore"
def name_for_ore_ee(otype, strata):
    return f"emendatusenigmatica:{otype.name}{strata.ee_suffix}_ore"
    
def ore_block_for_ore(otype, strata):
    if strata.name in otype.overrides:
        return otype.overrides[strata.name]
    elif not otype.custom and not strata.custom:
        return name_for_ore_ee(otype, strata)
    else:
        return f"constellation:{name_for_ore(otype, strata)}"
    
def record_for_pair(otype, strata):
    ee_exists = not otype.custom and not strata.custom
    block_name = ore_block_for_ore(otype, strata)

    record = types.SimpleNamespace()
    record.name = name_for_ore(otype, strata)
    record.ore_block = block_name
    record.otype = otype.name
    record.strata = strata.name
    record.needs_new_block = block_name.startswith("constellation:")
    
    if "overworld" in otype.categories or "twilight" in otype.categories:
        record.primary = strata.name == "stone"
    elif "nether" in otype.categories:
        record.primary = strata.name == "netherrack"
    elif "end" in otype.categories:
        record.primary = strata.name == "end_stone"
    
    record.categories = sorted(list(set(otype.categories).intersection(set(strata.categories))))
        
    return record

def is_strata_used(otype, strata):
    for category in strata.categories:
        if category in otype.categories:
            return True
    return False

# Creates a list of all ores we generate/need to generate.
all_ores = []
for strata in ore_stratas.values():
    for otype in ore_types.values():
        if (
            is_strata_used(otype, strata) and 
            not otype.disabled and not strata.disabled and 
            strata.name not in otype.no_generation
        ):
            all_ores.append(record_for_pair(otype, strata))            

# Find all unused EE ores to eventually remove them from JEI.
ee_unused = []
for strata in ore_stratas.values():
    for otype in ore_types.values():
        is_ee = not strata.custom and not otype.custom
        not_default = not ore_block_for_ore(otype, strata).startswith("emendatusenigmatica:")
        not_enabled = otype.disabled or strata.disabled or strata.name in otype.no_generation
        not_used = not is_strata_used(otype, strata)
        if is_ee and (not_default or not_enabled or not_used):
            ee_unused.append(name_for_ore_ee(otype, strata))

###########################
# Datapack generator code #
###########################

def make_i18n():
    for ore in all_ores:
        otype = ore_types[ore.otype]
        strata = ore_stratas[ore.strata]
        datapack.add_i18n(group(ore.ore_block), f"block.{group(ore.ore_block)}.{path(ore.ore_block)}", f"{strata.display_name} {otype.display_name} Ore")

def worldgen_for_ore(record, category):
    otype = ore_types[record.otype]
    strata = ore_stratas[record.strata]
    if not category in otype.worldgen:
        print(f"[ WARN ] Missing category {category} for {record.ore_block}")
        return ""
    data = otype.worldgen[category]
    
    if category == "overworld":
        biome_list_id = "ovw"
    elif category == "twilight":
        biome_list_id = "twf"
    else:
        biome_list_id = "all"
    return f"""add_gen_ore({
        repr(record.ore_block)}, {repr(ore_stratas[record.strata].parent_stone)},
        {data.cluster_size}, {data.cluster_count}, {data.min_y}, {data.max_y}, {biome_list_id}
    )\n"""
def make_worldgen():
    accum = ""
    for ore in all_ores:
        for category in ore.categories:
            accum += worldgen_for_ore(ore, category)
    datapack.add_startup_script("add_worldgen_ores", f"""
        {{
            let twb = {repr(twilight_forest_biomes)}
            let twf = {{ "blacklist": false, "values": twb }}
            let ovw = {{ "blacklist": true, "values": twb }}
            let all = {{ "blacklist": true, "values": [] }}
            {accum}
        }}
    """)

def make_blocks():
    accum = ""
    for ore in all_ores:
        if ore.needs_new_block:
            otype = ore_types[ore.otype]
            strata = ore_stratas[ore.strata]
            texture = f"{group(ore.ore_block)}:block/{path(ore.ore_block)}"
            accum += f"""gen_blk(
                {repr(ore.ore_block)}, {repr(f"{strata.display_name} {otype.display_name} Ore")}, {otype.strength}, {otype.resistance},
                {repr(strata.harvest_tool)}, {otype.harvest_level}, {repr(strata.material)},
                {repr(texture)}
            )\n"""
    datapack.add_startup_script("create_custom_ores", f"""
        onEvent('block.registry', event => {{
            let gen_blk = bind_gen_blk(event)
            {accum}
        }})
    """)
        
def make_textures():
    for ore in all_ores:
        otype = ore_types[ore.otype]
        strata = ore_stratas[ore.strata]

        if strata.name in otype.keep_texture:
            continue

        if ore.needs_new_block:
            texture = f"{group(ore.ore_block)}:block/{path(ore.ore_block)}"
        else:
            texture = f"constellation:block/{name_for_ore(otype, strata)}"
            json = {
                "parent": "block/cube_all",
                "textures": {
                    "all": texture,
                },
            }
            datapack.add_json_asset(f"{group(ore.ore_block)}/models/block/{path(ore.ore_block)}.json", json)
            
        target_path = f"{group(texture)}/textures/{path(texture)}.png"
        source_xcf = f"{mod_path}/ore_overlays.xcf"
        base_png = moddata.find_texture(ore_stratas[ore.strata].texture)
        datapack.compose_texture(target_path, source_xcf, ore.otype, base_png)

def make_loot_tables():
    for ore in all_ores:
        otype = ore_types[ore.otype]
        ore_block = ore.ore_block
        
        if otype.min_count == otype.max_count:
            count_func = otype.min_count
        else:
            count_func = { "min": otype.min_count, "max": otype.max_count, "type": "minecraft:uniform" }
        # TODO: Instead of this cluster/chunk hack, make a seperate raw ore type, probably?
        json = {
            "type": "minecraft:block",
            "pools": [
                {
                "rolls": 1,
                "entries": [{
                    "type": "minecraft:alternatives",
                    "children": [
                        {
                            "type": "minecraft:item",
                            "conditions": [{
                                "condition": "minecraft:match_tool",
                                "predicate": {
                                    "enchantments": [{
                                        "enchantment": "minecraft:silk_touch",
                                        "levels": { "min": 1 },
                                    }],
                                },
                            }],
                            "name": f"emendatusenigmatica:{otype.name}_cluster",
                        },
                        {
                            "type": "minecraft:item",
                            "functions": [
                                {
                                    "function": "minecraft:set_count",
                                    "count": count_func,
                                },
                                {
                                    "function": "minecraft:apply_bonus",
                                    "enchantment": "minecraft:fortune",
                                    "formula": "minecraft:ore_drops",
                                },
                                {
                                    "function": "minecraft:explosion_decay",
                                },
                            ],
                            "name": otype.drop_name or f"emendatusenigmatica:{otype.name}_chunk",
                        },
                    ],
                }],
            }],
        }
        datapack.add_json_data(f"{group(ore_block)}/loot_tables/blocks/{path(ore_block)}.json", json)

def remove_unused():
    for item in ee_unused:
        datapack.remove_name(item)
    for ore in all_ores:
        if not ore.primary:
            datapack.hide_name(ore.ore_block)

def make_tooltips():
    data = {}
    for ore in all_ores:
        if ore.primary:
            otype = ore_types[ore.otype]
            strata = ore_stratas[ore.strata]

            locales = []
            if "overworld" in otype.categories:
                locales.append("Overworld")
            if "twilight" in otype.categories:
                locales.append("Twilight Forest")
            if "nether" in otype.categories:
                locales.append("Nether")
            if "end" in otype.categories:
                locales.append("End")
                
            if len(locales) == 1:
                data[ore.ore_block] = locales[0]
            elif len(locales) == 2:
                data[ore.ore_block] = f"{locales[0]} and {locales[1]}"
            elif len(locales) >= 3:
                data[ore.ore_block] = f"{', '.join(locales[:-1])} and {locales[-1]})"
    
    datapack.add_client_script("worldgen_ore_locations", f"found_in_events({json.dumps(data)})")

def make_tags():
    for ore in all_ores:
        datapack.tags.add_both_tag(ore.ore_block, f"forge:ores")
        datapack.tags.add_both_tag(ore.ore_block, f"forge:ores/{ore.otype}")
        datapack.tags.add_both_tag(ore.ore_block, "constellation:generated_ores")

make_i18n()
make_worldgen()
make_blocks()
make_textures()
make_tags()
make_tooltips()
make_loot_tables()
remove_unused()
