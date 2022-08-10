import toml

from gen.utils import *

# TODO: Use EE-style graphics for Create/Blood Magic/Mekanism
# TODO: Unify deepslate

###############
# Definitions #
###############

# Definitions for unification
unify_list = [
    "coal", "iron", "gold", "diamond", "emerald", "lapis", "redstone", "quartz", "copper", # Vanilla
    "silver", "lead", "nickel", "uranium",  "osmium", "zinc", # Modded Metals
    "bronze", "brass", "constantan", "electrum", "steel", "invar", "signalum", "lumium", "enderium", # Alloys
]
unify_groups = [
    "chunks", "dusts", "gears", "gems", "ingots", "nuggets", "plates", "rods", "wires", # Ingredients
    "mekanism:clumps", "mekanism:crystals", "mekanism:dirty_dusts", "mekanism:shards", # Mekanism ore processing
    "create:crushed_ores", "bloodmagic:fragments", "bloodmagic:gravels", # Other ore processing
]

preference_list = ["minecraft", "cavesandcliffs", "emendatusenigmatica", "createaddition", "immersiveengineering", "silentgear"]

# Definitions for EE items
ore_processing_gems = [
    "coal", "diamond", "emerald", "lapis", "quartz", "fluorite", "bitumen", "cinnabar", "apatite", "sulfur",
    "arcane", "dimensional", "ruby", "sapphire", "peridot",
]
ore_processing_dust = ["redstone"]

tag_slurries = ["aluminum", "nickel", "silver", "thallasium", "zinc"]

# Definitions for unused technical mod items
unused_gears = [
    "lapis", "quartz", "enderium", "emerald", "uranium", "osmium", "zinc", "brass", "steel", "cast_iron", "redstone",
]
unused_materials = [
    "certus_quartz", "charged_certus_quartz", "fluix", "potassium_nitrate",
    "iesnium", "regalium", "utherium", "froststeel", "cloggrum", "nebu",
    "cast_iron", "iridium", "cobalt", "aluminum",
]

########
# Code #
########

def delete_item(datapack, item, tag):
    if item in datapack.tags.get_item_tag(tag):
        datapack.remove_name(item)
        datapack.tags.remove_tag(["blocks", "items"], item, [tag, tag.split("/")[0]])
def unify_tags(datapack):
    accum = ""
    preferred = {}
    has_kind = {}
    
    # Find preferred items
    for kind in unify_list:
        has_kind.setdefault(kind, set({})) # ensure group exists
        for unify_group in unify_groups:
            if ":" not in unify_group:
                unify_group = f"forge:{unify_group}"
            tag = f"{unify_group}/{kind}"
            items = sorted(datapack.tags.get_item_tag(tag))
            if len(items) != 0:
                found_item = None
                
                for item in items:
                    for test_group in preference_list:
                        if group(item) == test_group:
                            found_item = item
                            break
                    if found_item != None:
                        break
                preferred[tag] = found_item or items[0]
                has_kind.setdefault(kind, set({})).add(unify_group)
                
    # Remove non-preferred items
    for tag in preferred:
        items = sorted(datapack.tags.get_item_tag(tag))
        for item in items:
            if item != preferred[tag]:
                datapack.remove_name(item)
                
    # Removed unused items
    for kind in unused_materials + unused_gears:
        datapack.remove_name(f"emendatusenigmatica:{kind}_gear")
    for kind in unused_materials + ore_processing_gems:
        delete_item(datapack, f"emendatusenigmatica:{kind}_clump", f"mekanism:clumps/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_crystal", f"mekanism:crystals/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_dirty_dust", f"mekanism:dirty_dusts/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_shard", f"mekanism:shards/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_fragment", f"bloodmagic:fragments/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_gravel", f"bloodmagic:gravels/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_crushed", f"create:crushed_ores/{kind}")
    for kind in unused_materials:
        delete_item(datapack, f"emendatusenigmatica:{kind}_ingot", f"forge:ingots/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_block", f"forge:storage_blocks/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_nugget", f"forge:nuggets/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_gem", f"forge:gems/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_dust", f"forge:dusts/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_chunk", f"forge:chunks/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_cluster", f"forge:clusters/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_plate", f"forge:plates/{kind}")
        delete_item(datapack, f"emendatusenigmatica:{kind}_rod", f"forge:rods/{kind}")
        
    # Remove molten metals entirely. (No Tinker's Construct)
    for item in list(datapack.tags.get_item_tag("constellation:remove_buckets")):
        datapack.remove_name(item)
    for item in list(datapack.tags.get_item_tag("constellation:remove_molten")):
        datapack.remove_name(item)
    
    # Mark clusters as ores
    for kind in unify_list:
        cluster_name = f"emendatusenigmatica:{kind}_cluster"
        if cluster_name in datapack.tags.get_item_tag(f"forge:clusters/{kind}"):
            datapack.tags.add_item_tag(cluster_name, f"forge:ores/{kind}")

    # Mark slurries as slurries
    for kind in tag_slurries:
        datapack.tags.add_tag("slurries", f"emendatusenigmatica:dirty_{kind}", f"mekanism:dirty/{kind}")
        datapack.tags.add_tag("slurries", f"emendatusenigmatica:clean_{kind}", f"mekanism:clean/{kind}")
    
    # Unify smelting recipies
    for kind in unify_list:
        if "forge:ingots" in has_kind[kind]:
            accum += f"r.unify_ingot({repr(kind)})\n"
    
    # Generate script
    datapack.add_server_script("unify_materials", f"""
        onEvent('recipes', e => {{
            var r = bind_recipies(e, {repr(preferred)})
            {accum}
        }})
    """)

def write_configs():
    with open("configs/jaopca_main.toml") as fd:
        main = toml.loads(fd.read())
    main["itemSelection"]["preferredMods"] = preference_list
    with open("../config/jaopca/main.toml", "w") as fd:
        fd.write(toml.dumps(main))
