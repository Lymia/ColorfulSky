import toml
import types

from gen.utils import *

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

def add_type(name, strength, resistance, harvest_level, kind, *categories, disabled=False):
    record = types.SimpleNamespace()
    record.name = name
    record.custom = False
    record.disabled = disabled
    record.strength = strength
    record.resistance = resistance
    record.harvest_level = harvest_level
    record.kind = kind
    record.categories = categories
    record.worldgen = {}
    record.overrides = {}
    record.spawn_modifier = {}
    ore_types[record.name] = record
def add_worldgen(name, cluster_size, cluster_count, chance, height_range, target="default"):
    record = types.SimpleNamespace()
    record.cluster_size = cluster_size
    record.cluster_count = cluster_count
    record.chance = chance
    record.min_y = height_range[0]
    record.max_y = height_range[1]
    ore_types[name].worldgen[target] = record
def add_ore_override(name, strata, block):
    ore_types[name].overrides[strata] = block

def add_strata(name, texture, parent_stone, category, is_custom=False, disabled=False):
    record = types.SimpleNamespace()
    record.name = name
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
    record.category = category
    ore_stratas[record.name] = record

# EE built-in types
add_type("coal", 3, 3, 0, "gem", "overworld", "twilightforest")
add_type("iron", 3, 3, 1, "metal", "overworld", "twilightforest")
add_type("gold", 3, 3, 2, "metal", "overworld", "twilightforest", "nether")
add_type("diamond", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("emerald", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("lapis", 3, 3, 1, "gem", "overworld", "twilightforest", "nether")
add_type("redstone", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("quartz", 3, 3, 2, "gem", "overworld", "nether")
add_type("copper", 3, 3, 1, "ingot", "overworld", "twilightforest")
add_type("aluminum", 3, 3, 1, "ingot", "overworld", "twilightforest", "end")
add_type("silver", 3, 3, 2, "ingot", "overworld", "twilightforest", "end")
add_type("lead", 3, 3, 2, "ingot", "overworld")
add_type("nickel", 3, 3, 2, "ingot", "overworld")
add_type("uranium", 3, 3, 2, "ingot", "overworld", "nether")
add_type("osmium", 3, 3, 1, "ingot", "overworld", "end")
add_type("fluorite", 3, 3, 1, "gem", "overworld", "end")
add_type("apatite", 3, 3, 1, "gem", "overworld", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("sulfur", 3, 3, 1, "gem", "overworld", "nether")
add_type("dimensional", 3, 3, 1, "gem", "overworld", "twilightforest", "nether", "end")
add_type("arcane", 3, 3, 1, "gem", "overworld", "twilightforest", "end")

add_type("bitumen", 3, 3, 0, "-", "-", disabled = True)
add_type("cinnabar", 3, 3, 0, "-", "-", disabled = True)
add_type("certus_quartz", 3, 3, 0, "-", "-", disabled = True)
add_type("charged_certus_quartz", 3, 3, 0, "-", "-", disabled = True)
add_type("cobalt", 3, 3, 0, "-", "-", disabled = True)
add_type("iridium", 3, 3, 0, "-", "-", disabled = True)
add_type("nickel", 3, 3, 0, "-", "-", disabled = True)
add_type("peridot", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("potassium_nitrate", 3, 3, 0, "-", "-", disabled = True)
add_type("ruby", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("sapphire", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("zinc", 3, 3, 0, "-", "-", disabled = True)

# EE built-in strata
add_strata("stone", "minecraft:block/stone", "minecraft:stone", "overworld")
add_strata("andesite", "minecraft:block/andesite",  "minecraft:andesite", "overworld")
add_strata("granite", "minecraft:block/granite",  "minecraft:granite", "overworld")
add_strata("diorite", "minecraft:block/diorite",  "minecraft:diorite", "overworld")
add_strata("sand", None, None, "overworld", disabled=True)
add_strata("gravel", None, None, "overworld", disabled=True)
add_strata("netherrack", "minecraft:block/netherrack",  "minecraft:netherrack", "nether")
add_strata("blackstone", "minecraft:block/blackstone",  "minecraft:blackstone", "nether")
add_strata("basalt", "minecraft:block/basalt_side",  "minecraft:basalt", "nether")
add_strata("soul_soil", "minecraft:block/soul_soil",  "minecraft:soul_soil", "nether")
add_strata("end_stone", "minecraft:block/end_stone",  "minecraft:end_stone", "end")

add_strata("gabbro", None, None, "overworld", disabled=True)
add_strata("c_limestone", None, None, "overworld", disabled=True),
add_strata("scoria", None, None, "overworld", disabled=True),
add_strata("weathered_limestone", None, None, "overworld", disabled=True),

add_strata("jasper", "quark:block/jasper", "quark:jasper", "overworld")
add_strata("marble", "quark:block/marble", "quark:marble", "overworld")
add_strata("slate", "quark:block/slate", "quark:slate", "overworld")
add_strata("deepslate", "quark:block/backport/deepslate", "quark:deepslate", "overworld")

add_strata("mossy_stone", "byg:block/mossy_stone", "byg:mossy_stone", "overworld")
add_strata("brimstone", "byg:block/brimstone", "byg:brimstone", "nether")
add_strata("subzero_ash", "byg:block/subzero_ash", "byg:subzero_ash_block", "nether")
add_strata("blue_netherrack", "byg:block/blue_netherrack", "byg:blue_netherrack", "nether")
add_strata("nylium_soul_soil", "byg:block/nylium_soul_soil", "byg:nylium_soul_soil", "nether")
add_strata("ether_stone", "byg:block/ether_stone", "byg:ether_stone", "nether")
add_strata("cryptic_stone", "byg:block/cryptic_stone", "byg:cryptic_stone", "nether")

add_strata("flavolite", "betterendforge:block/flavolite", "betterendforge:flavolite", "end")
add_strata("sulphuric_rock", "betterendforge:block/sulphuric_rock", "betterendforge:sulphuric_rock", "end")
add_strata("violecite", "betterendforge:block/violecite", "betterendforge:violecite", "end")

add_strata("raw_marble", "astralsorcery:block/marble_raw", "astralsorcery:marble_raw", "overworld")

# Custom strata
# TODO

# Ore overrides
add_ore_override("coal", "stone", "minecraft:coal_ore")
add_ore_override("coal", "deepslate", "cavesandcliffs:deepslate_coal_ore")
add_ore_override("iron", "stone", "minecraft:iron_ore")
add_ore_override("iron", "deepslate", "cavesandcliffs:deepslate_iron_ore")
add_ore_override("gold", "stone", "minecraft:gold_ore")
add_ore_override("gold", "deepslate", "cavesandcliffs:deepslate_gold_ore")
add_ore_override("diamond", "stone", "minecraft:diamond_ore")
add_ore_override("diamond", "deepslate", "cavesandcliffs:deepslate_diamond_ore")
add_ore_override("copper", "stone", "cavesandcliffs:copper_ore")
add_ore_override("copper", "deepslate", "cavesandcliffs:deepslate_copper_ore")
add_ore_override("redstone", "stone", "minecraft:redstone_ore")
add_ore_override("redstone", "deepslate", "cavesandcliffs:deepslate_redstone_ore")
add_ore_override("lapis", "stone", "minecraft:lapis_ore")
add_ore_override("lapis", "deepslate", "cavesandcliffs:deepslate_lapis_ore")
add_ore_override("emerald", "stone", "minecraft:emerald_ore")
add_ore_override("emerald", "deepslate", "cavesandcliffs:deepslate_emerald_ore")

############################
# Worldgen from EE configs #
############################

def extract_worldgen(section, name, kind):
    location_avg = section[f"{kind}_base"]
    location_spread = section[f"{kind}_spread"]
    cluster_count = section[f"{kind}_count"]
    cluster_size = section[f"{kind}_size"]
    
    min_y = location_avg - location_spread
    max_y = location_avg + location_spread
    
    add_worldgen(name, cluster_size, cluster_count, 1, (min_y, max_y), target = kind)
    if kind == "overworld":
        add_worldgen(name, cluster_size, cluster_count, 1, (min_y, max_y))
def parse_toml():
    ee_config = toml.loads(open("configs/emendatusenigmatica-common.toml").read())
    for otype in ore_types.values():
        for section in ee_config:
            if otype.name in section.lower() and not "Certus" in section:
                section = ee_config[section]
                extract_worldgen(section["Overworld"], otype.name, "overworld")
                extract_worldgen(section["The Nether"], otype.name, "nether")
                extract_worldgen(section["The End"], otype.name, "end")
                break
parse_toml()

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
        return f"colorfulsky:{name_for_ore(otype, strata)}"
    
def record_for_pair(otype, strata):
    ee_exists = not otype.custom and not strata.custom
    block_name = ore_block_for_ore(otype, strata)

    record = types.SimpleNamespace()
    record.name = name_for_ore(otype, strata)
    record.ore_block = block_name
    record.otype = otype.name
    record.strata = strata.name
    record.needs_new_block = block_name.startswith("colorfulsky:")
    return record

# Creates a list of all ores we generate/need to generate.
all_ores = []
for otype in ore_types.values():
    for strata in ore_stratas.values():
        if strata.category in otype.categories and not otype.disabled and not strata.disabled:
            all_ores.append(record_for_pair(otype, strata))            

# Find all unused EE ores to eventually remove them from JEI.
ee_unused = []
for otype in ore_types.values():
    for strata in ore_stratas.values():
        is_ee = not strata.custom and not otype.custom
        not_default = not ore_block_for_ore(otype, strata).startswith("emendatusenigmatica:")
        not_enabled = otype.disabled or strata.disabled
        if is_ee and (not_default or not_enabled):
            ee_unused.append(name_for_ore_ee(otype, strata))

###########################
# Datapack generator code #
###########################

def worldgen_data(record):
    category = ore_stratas[record.strata].category
    if category in ore_types[record.otype].worldgen:
        return ore_types[record.otype].worldgen[category]
    elif "default" in ore_types[record.otype].worldgen:
        return ore_types[record.otype].worldgen["default"]
    else:
        return None
def worldgen_for_ore(record):
    otype = ore_types[record.otype]
    strata = ore_stratas[record.strata]
    data = worldgen_data(record)
    if data == None:
        return ""
    else:
        biome_list_id = "all"
        if strata.category == "overworld":
            twf = "twilightforest" in otype.categories
            ovw = "overworld" in otype.categories
            if twf and not ovw:
                biome_list_id = "twf"
            if not twf and ovw:
                biome_list_id = "ovw"
        
        return f"""gen_ore({
            repr(record.ore_block)}, {repr(ore_stratas[record.strata].parent_stone)}, 
            {data.cluster_size}, {data.cluster_count}, {data.min_y}, {data.max_y}, {biome_list_id}
        )\n"""
def make_worldgen():
    accum = ""
    for ore in all_ores:
        accum += worldgen_for_ore(ore)
    js = f"""
        onEvent('worldgen.add', event => {{
            var twb = {repr(twilight_forest_biomes)}
            var twf = {{ "blacklist": false, "values": twb }}
            var ovw = {{ "blacklist": true, "values": twb }}
            var all = {{ "blacklist": true, "values": [] }}
            var gen_ore = function(block, parent_stone, cluster_size, cluster_count, min_y, max_y, biomes) {{
                if(!Block.getBlock(block)) console.error(`No such block: ${{block}}`);
                if(parent_stone[0] != "#" && !Block.getBlock(parent_stone)) console.error(`No such block: ${{parent_stone}}`);
                event.addOre(ore => {{
                    ore.block = block
                    ore.spawnsIn.blacklist = false
                    ore.spawnsIn.values = [parent_stone]
                    ore.biomes = biomes
                    ore.biomes.blacklist = biome_blacklist
                    ore.biomes.values = biomes
                    ore.clusterMinSize = cluster_size
                    ore.clusterMaxSize = cluster_size
                    ore.clusterCount = cluster_count
                    ore.minHeight = min_y
                    ore.maxHeight = max_y
                    ore.squared = true
                    ore.setWorldgenLayer('vegetal_decoration') // as late as practical for purposes of avoiding later layers changing the stone type on us
                }})
            }}
            {accum}
        }})
    """
    return f"// Autogenerated by build script\n{js_minify_simple(js)}\n"
