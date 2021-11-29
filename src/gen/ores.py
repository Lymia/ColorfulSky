import toml
import types

from gen.utils import *

# TODO: Sided blocks (Grimestone, Blackstone, Brimstone, Basalt, Scoria)
# TODO: Make Soulium a normal ore
# TODO: Darker Depths unneeded definitions
# TODO: Some external ores in Blue Skies world.
# TODO: Figure out how to unscrew Alfheim

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

def add_type(name, display_name, strength, resistance, harvest_level, kind, *categories, is_custom=False, disabled=False):
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
    record.no_generation = set({})
    record.spawn_modifier = {}
    if is_custom:
        record.texture = f"constellation:blocks/ore_overlays/{name}"
    else:
        record.texture = f"emendatusenigmatica:blocks/overlays/{name}"
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
def add_unneeded(name, strata):
    ore_types[name].no_generation.add(strata)

def add_strata(name, display_name, texture, parent_stone, category, is_custom=False, disabled=False, material="stone", harvest_tool="pickaxe"):
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
    record.category = category
    record.material = material
    record.harvest_tool = harvest_tool
    ore_stratas[record.name] = record

# EE built-in types
add_type("coal", "Coal", 3, 3, 0, "gem", "overworld", "twilightforest")
add_type("iron", "Iron", 3, 3, 1, "metal", "overworld", "twilightforest")
add_type("gold", "Gold", 3, 3, 2, "metal", "overworld", "twilightforest", "nether")
add_type("diamond", "Diamond", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("emerald", "Emerald", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("lapis", "Lapis", 3, 3, 1, "gem", "overworld", "twilightforest", "nether")
add_type("redstone", "Redstone", 3, 3, 2, "gem", "overworld", "twilightforest")
add_type("quartz", "Quartz", 3, 3, 2, "gem", "overworld", "nether")
add_type("copper", "Copper", 3, 3, 1, "ingot", "overworld", "twilightforest")
add_type("aluminum", "Aluminum", 3, 3, 1, "ingot", "overworld", "twilightforest", "end")
add_type("silver", "Silver", 3, 3, 2, "ingot", "overworld", "twilightforest", "end")
add_type("lead", "Lead", 3, 3, 2, "ingot", "overworld")
add_type("nickel", "Nickel", 3, 3, 2, "ingot", "overworld")
add_type("uranium", "Uranium", 3, 3, 2, "ingot", "overworld", "nether")
add_type("osmium", "Osmium", 3, 3, 1, "ingot", "overworld", "end")
add_type("zinc", "Zinc", 3, 3, 2, "ingot", "overworld", "end")
add_type("fluorite", "Fluorite", 3, 3, 1, "gem", "overworld", "end")
add_type("apatite", "Apatite", 3, 3, 1, "gem", "overworld", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("sulfur", "Sulfur", 3, 3, 1, "gem", "overworld", "nether")
add_type("arcane", "Source Gem", 3, 3, 1, "gem", "overworld", "twilightforest", "end")
add_type("dimensional", "Dimensional Shard", 3, 3, 1, "gem", "overworld", "twilightforest", "nether", "end")

add_type("bitumen", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("cinnabar", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("certus_quartz", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("charged_certus_quartz", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("cobalt", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("iridium", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("nickel", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("peridot", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("potassium_nitrate", "-", 3, 3, 0, "-", "-", disabled = True)
add_type("ruby", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems
add_type("sapphire", "-", 3, 3, 0, "-", "-", disabled = True) # TODO: Figure out how to handle this and Silent's Gems

# EE built-in strata
add_strata("stone", "Stone", "minecraft:block/stone", "minecraft:stone", "overworld")
add_strata("andesite", "Andesite", "minecraft:block/andesite",  "minecraft:andesite", "overworld")
add_strata("granite", "Granite", "minecraft:block/granite",  "minecraft:granite", "overworld")
add_strata("diorite", "Diorite", "minecraft:block/diorite",  "minecraft:diorite", "overworld")
add_strata("sand", "Sand", None, None, "overworld", disabled=True)
add_strata("gravel", "Gravel", None, None, "overworld", disabled=True)
add_strata("netherrack", "Netherrack", "minecraft:block/netherrack",  "minecraft:netherrack", "nether")
add_strata("blackstone", "Blackstone", "minecraft:block/blackstone",  "minecraft:blackstone", "nether")
add_strata("basalt", "Basalt", "minecraft:block/basalt_side",  "minecraft:basalt", "nether")
add_strata("end_stone", "End Stone", "minecraft:block/end_stone",  "minecraft:end_stone", "end")
add_strata("soul_soil", "Soul Soil", "minecraft:block/soul_soil",  "minecraft:soul_soil", "nether", disabled=True)

add_strata("gabbro", "Gabbro", "create:block/palettes/gabbro/plain", "create:gabbro", "overworld")
add_strata("c_limestone", "Limestone", "create:block/palettes/limestone/plain", "create:limestone", "overworld", disabled=True),
add_strata("scoria", "Scoria", "create:block/palettes/natural_scoria", "create:natural_scoria", "overworld"),
add_strata("weathered_limestone", "Weathered Limestone", "create:block/palettes/weathered_limestone/plain", "create:weathered_limestone", "overworld"),

add_strata("jasper", "Jasper", "quark:block/jasper", "quark:jasper", "overworld")
add_strata("marble", "Marble", "quark:block/marble", "quark:marble", "overworld")
add_strata("slate", "Slate", "quark:block/slate", "quark:slate", "overworld")
add_strata("deepslate", "Deepslate", "quark:block/backport/deepslate", "quark:deepslate", "overworld")

add_strata("mossy_stone", "Mossy Stone", "byg:block/mossy_stone", "byg:mossy_stone", "overworld")
add_strata("brimstone", "Brimstone", "byg:block/brimstone", "byg:brimstone", "nether")
add_strata("subzero_ash", "Subzero Ash", "byg:block/subzero_ash", "byg:subzero_ash_block", "nether", disabled=True)
add_strata("blue_netherrack", "Blue Netherrack", "byg:block/blue_netherrack", "byg:blue_netherrack", "nether")
add_strata("nylium_soul_soil", "Nylium Soul Soil", "byg:block/nylium_soul_soil", "byg:nylium_soul_soil", "nether", disabled=True)
add_strata("ether_stone", "Ether Stone", "byg:block/ether_stone", "byg:ether_stone", "nether")
add_strata("cryptic_stone", "Cryptic Stone", "byg:block/cryptic_stone", "byg:cryptic_stone", "nether")

add_strata("flavolite", "Flavolite", "betterendforge:block/flavolite", "betterendforge:flavolite", "end")
add_strata("sulphuric_rock", "Sulphuric Rock", "betterendforge:block/sulphuric_rock", "betterendforge:sulphuric_rock", "end")
add_strata("violecite", "Violecite", "betterendforge:block/violecite", "betterendforge:violecite", "end")

add_strata("raw_marble", "Marble", "astralsorcery:block/marble_raw", "astralsorcery:marble_raw", "overworld", disabled=True)

# Custom strata
add_strata("clay", "Clay", "minecraft:block/clay", "minecraft:clay", "overworld", is_custom=True, material="clay", harvest_tool="shovel")
add_strata("dolomite", "Dolomite", "create:block/palettes/dolomite/plain", "create:dolomite", "overworld", is_custom=True)
add_strata("aridrock", "Aridrock", "darkerdepths:block/aridrock", "darkerdepths:aridrock", "overworld", is_custom=True)
add_strata("grimestone", "Grimestone", "darkerdepths:block/grimestone", "darkerdepths:grimestone", "overworld", is_custom=True)
add_strata("dd_limestone", "Limestone", "darkerdepths:block/limestone", "darkerdepths:limestone", "overworld", is_custom=True)
add_strata("dacite", "Dacite", "byg:block/dacite", "byg:dacite", "overworld", is_custom=True)
add_strata("red_rock", "Red Rock", "byg:block/red_rock", "byg:red_rock", "overworld", is_custom=True)
add_strata("travertine", "Travertine", "byg:block/travertine", "byg:travertine", "overworld", is_custom=True)
add_strata("soapstone", "Soapstone", "byg:block/soapstone", "byg:soapstone", "overworld", is_custom=True)
add_strata("q_limestone", "Limestone", "quark:block/limestone", "quark:limestone", "overworld", is_custom=True)

add_strata("quartzite", "Quartzite", "byg:block/quartzite_sand", "byg:quartzite_sand", "nether", is_custom=True, material="sand", harvest_tool="shovel")
add_strata("scoria_stone", "Scoria Stone", "byg:block/scoria_stone", "byg:scoria_stone", "nether", is_custom=True),
add_strata("s_soul_soil", "Soul Soil", "minecraft:block/soul_soil",  "minecraft:soul_soil", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("s_nylium_soul_soil", "Nylium Soul Soil", "byg:block/nylium_soul_soil", "byg:nylium_soul_soil", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("s_subzero_ash", "Subzero Ash", "byg:block/subzero_ash", "byg:subzero_ash_block", "nether", is_custom=True, material="dirt", harvest_tool="shovel")
add_strata("dullstone", "Dullstone", "infernalexp:block/dullstone", "infernalexp:dullstone", "nether", is_custom=True),
add_strata("shimmerstone", "Shimmerstone", "infernalexp:block/glowdust_stone", "infernalexp:glowdust_stone", "nether", is_custom=True),

# Ore overrides
for ore in ["coal", "iron", "gold", "diamond", "redstone", "lapis", "emerald"]:
    add_ore_override(ore, "stone", f"minecraft:{ore}_ore")
    add_ore_override(ore, "deepslate", f"cavesandcliffs:deepslate_{ore}_ore")
add_ore_override("copper", "stone", "cavesandcliffs:copper_ore")
add_ore_override("copper", "deepslate", "cavesandcliffs:deepslate_copper_ore")

# Unneeded ores
add_unneeded("quartz", "quartzite")

####################
# Worldgen configs #
####################

add_worldgen('coal', 17, 15, 1, (0, 120), target = 'overworld')
add_worldgen('coal', 17, 15, 1, (30, 150), target = 'nether')
add_worldgen('coal', 17, 15, 1, (20, 140), target = 'end')
add_worldgen('iron', 11, 17, 1, (0, 64), target = 'overworld')
add_worldgen('iron', 11, 17, 1, (30, 94), target = 'nether')
add_worldgen('iron', 11, 17, 1, (20, 84), target = 'end')
add_worldgen('gold', 8, 7, 1, (0, 32), target = 'overworld')
add_worldgen('gold', 8, 7, 1, (30, 62), target = 'nether')
add_worldgen('gold', 8, 7, 1, (20, 52), target = 'end')
add_worldgen('diamond', 8, 3, 1, (0, 16), target = 'overworld')
add_worldgen('diamond', 8, 3, 1, (30, 46), target = 'nether')
add_worldgen('diamond', 8, 3, 1, (20, 36), target = 'end')
add_worldgen('emerald', 4, 3, 1, (100, 212), target = 'overworld')
add_worldgen('emerald', 4, 3, 1, (72, 184), target = 'nether')
add_worldgen('emerald', 4, 3, 1, (120, 232), target = 'end')
add_worldgen('lapis', 7, 4, 1, (0, 16), target = 'overworld')
add_worldgen('lapis', 7, 4, 1, (30, 46), target = 'nether')
add_worldgen('lapis', 7, 4, 1, (20, 36), target = 'end')
add_worldgen('redstone', 11, 8, 1, (0, 16), target = 'overworld')
add_worldgen('redstone', 11, 8, 1, (30, 46), target = 'nether')
add_worldgen('redstone', 11, 8, 1, (20, 36), target = 'end')
add_worldgen('quartz', 14, 16, 1, (10, 110), target = 'overworld')
add_worldgen('quartz', 14, 16, 1, (40, 140), target = 'nether')
add_worldgen('quartz', 14, 16, 1, (30, 130), target = 'end')
add_worldgen('copper', 7, 17, 1, (44, 60), target = 'overworld')
add_worldgen('copper', 7, 17, 1, (74, 90), target = 'nether')
add_worldgen('copper', 7, 17, 1, (64, 80), target = 'end')
add_worldgen('aluminum', 5, 8, 1, (50, 70), target = 'overworld')
add_worldgen('aluminum', 5, 8, 1, (80, 100), target = 'nether')
add_worldgen('aluminum', 5, 8, 1, (70, 90), target = 'end')
add_worldgen('silver', 5, 8, 1, (30, 38), target = 'overworld')
add_worldgen('silver', 5, 8, 1, (60, 68), target = 'nether')
add_worldgen('silver', 5, 8, 1, (50, 58), target = 'end')
add_worldgen('lead', 5, 8, 1, (32, 40), target = 'overworld')
add_worldgen('lead', 5, 8, 1, (62, 70), target = 'nether')
add_worldgen('lead', 5, 8, 1, (52, 60), target = 'end')
add_worldgen('nickel', 4, 8, 1, (24, 40), target = 'overworld')
add_worldgen('nickel', 4, 8, 1, (54, 70), target = 'nether')
add_worldgen('nickel', 4, 8, 1, (44, 60), target = 'end')
add_worldgen('uranium', 6, 6, 1, (4, 20), target = 'overworld')
add_worldgen('uranium', 6, 6, 1, (34, 50), target = 'nether')
add_worldgen('uranium', 6, 6, 1, (24, 40), target = 'end')
add_worldgen('osmium', 6, 15, 1, (20, 44), target = 'overworld')
add_worldgen('osmium', 6, 15, 1, (50, 74), target = 'nether')
add_worldgen('osmium', 6, 15, 1, (40, 64), target = 'end')
add_worldgen('zinc', 5, 9, 1, (34, 50), target = 'overworld')
add_worldgen('zinc', 5, 9, 1, (64, 80), target = 'nether')
add_worldgen('zinc', 5, 9, 1, (54, 70), target = 'end')
add_worldgen('fluorite', 9, 5, 1, (0, 32), target = 'overworld')
add_worldgen('fluorite', 9, 5, 1, (30, 62), target = 'nether')
add_worldgen('fluorite', 9, 5, 1, (20, 52), target = 'end')
add_worldgen('apatite', 22, 2, 1, (64, 128), target = 'overworld')
add_worldgen('apatite', 22, 2, 1, (94, 158), target = 'nether')
add_worldgen('apatite', 22, 2, 1, (84, 148), target = 'end')
add_worldgen('sulfur', 7, 3, 1, (0, 16), target = 'overworld')
add_worldgen('sulfur', 7, 3, 1, (30, 46), target = 'nether')
add_worldgen('sulfur', 7, 3, 1, (20, 36), target = 'end')
add_worldgen('arcane', 6, 5, 1, (20, 46), target = 'overworld')
add_worldgen('arcane', 6, 5, 1, (50, 76), target = 'nether')
add_worldgen('arcane', 6, 5, 1, (40, 66), target = 'end')
add_worldgen('dimensional', 2, 2, 1, (0, 20), target = 'overworld')
add_worldgen('dimensional', 2, 2, 1, (30, 50), target = 'nether')
add_worldgen('dimensional', 2, 2, 1, (20, 40), target = 'end')

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
    return record

# Creates a list of all ores we generate/need to generate.
all_ores = []
for strata in ore_stratas.values():
    for otype in ore_types.values():
        if (
            strata.category in otype.categories and 
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
        not_used = strata.category not in otype.categories
        if is_ee and (not_default or not_enabled or not_used):
            ee_unused.append(name_for_ore_ee(otype, strata))

###########################
# Datapack generator code #
###########################

def make_i18n(datapack):
    for ore in all_ores:
        otype = ore_types[ore.otype]
        strata = ore_stratas[ore.strata]
        datapack.add_i18n(group(ore.ore_block), f"block.{group(ore.ore_block)}.{path(ore.ore_block)}", f"{strata.display_name} {otype.display_name} Ore")

def worldgen_data(record):
    category = ore_stratas[record.strata].category
    if category in ore_types[record.otype].worldgen:
        return ore_types[record.otype].worldgen[category]
    elif "overworld" in ore_types[record.otype].worldgen:
        return ore_types[record.otype].worldgen["overworld"]
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
def make_worldgen(datapack):
    accum = ""
    for ore in all_ores:
        accum += worldgen_for_ore(ore)
        datapack.tags.add_both_tag(ore.ore_block, f"forge:ores")
        datapack.tags.add_both_tag(ore.ore_block, f"forge:ores/{ore.otype}")
    datapack.add_script("add_worldgen_ores", f"""
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
                    ore.biomes.blacklist = biomes.blacklist
                    ore.biomes.values = biomes.values
                    ore.clusterMinSize = cluster_size
                    ore.clusterMaxSize = cluster_size
                    ore.clusterCount = cluster_count
                    ore.minHeight = min_y
                    ore.maxHeight = max_y
                    ore.squared = true
                    ore.setWorldgenLayer('top_layer_modification')
                }})
            }}
            {accum}
        }})
    """)

def make_blocks(datapack, moddata):
    accum = ""
    for ore in all_ores:
        if ore.needs_new_block:
            otype = ore_types[ore.otype]
            strata = ore_stratas[ore.strata]
            texture = f"constellation:block/{ore.name}"
            compose_textures(moddata, texture, ore_stratas[ore.strata].texture, ore_types[ore.otype].texture)
            accum += f"""gen_blk(
                {repr(ore.ore_block)}, {otype.strength}, {otype.resistance},
                {repr(strata.harvest_tool)}, {otype.harvest_level}, {repr(strata.material)},
                {repr(texture)}
            )\n"""
    datapack.add_script("create_custom_ores", f"""
        onEvent('block.registry', event => {{
            var gen_blk = function(ore_name, hardness, resistance, harvest_tool, harvest_level, material, texture) {{
                var block = event.create(ore_name)
                block.material(material).fullBlock(true).texture(texture)
                block.requiresTool(true).hardness(hardness).resistance(resistance).harvestTool(harvest_tool, harvest_level)
            }}
            {accum}
        }})
    """)

def remove_unused(datapack):
    for item in ee_unused:
        datapack.remove_name(item)

def make_ores(datapack, moddata):
    make_i18n(datapack)
    make_worldgen(datapack)
    make_blocks(datapack, moddata)
    remove_unused(datapack)
