import toml

from pack_helper.ctx import *
from pack_helper.utils import *

# TODO: Use EE-style graphics for Create/Blood Magic/Mekanism
# TODO: Fluid unification

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

tag_slurries = [
    "aluminum", "apatite", "arcane", "bitumen", "certus_quartz", "charged_certus_quartz", "cinnabar", "cloggrum", "coal", "cobalt",
    "diamond", "dimensional", "emerald", "fluorite", "froststeel", "iesnium", "iridium", "lapis_lazuli", "nebu", "nickel", "peridot",
    "potassium_nitrate", "quartz", "redstone", "regalium", "ruby", "sapphire", "silver", "sulfur", "thallasium", "utherium", "zinc",
]

# Definitions for unused technical mod items
unused_gears = [
    "lapis", "quartz", "enderium", "emerald", "uranium", "osmium", "zinc", "brass", "steel", "cast_iron", "redstone",
]
unused_materials = [
    "certus_quartz", "charged_certus_quartz", "fluix", "potassium_nitrate", "iesnium", "regalium", "utherium", "froststeel",
    "cloggrum", "nebu","cast_iron", "iridium", "cobalt", "aluminum", "ender",
]

########
# Code #
########

def delete_item(item, tag):
    if item in datapack.tags.get_item_tag(tag) or item in datapack.tags.get_fluid_tag(tag) or item in datapack.tags.get_slurry_tag(tag):
        datapack.remove_name(item)
def unify_tags():
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
                datapack.unify_name(item)
            
    # Mark clusters as ores
    for kind in unify_list:
        cluster_name = f"emendatusenigmatica:{kind}_cluster"
        if cluster_name in datapack.tags.get_item_tag(f"forge:clusters/{kind}"):
            datapack.tags.add_item_tag(cluster_name, f"forge:ores/{kind}")

    # Mark slurries as slurries
    for kind in tag_slurries:
        datapack.tags.add_tag("slurries", f"emendatusenigmatica:dirty_{kind}", f"mekanism:dirty/{kind}")
        datapack.tags.add_tag("slurries", f"emendatusenigmatica:clean_{kind}", f"mekanism:clean/{kind}")
                
    # Removed unused items
    for kind in unused_materials + unused_gears:
        datapack.unify_name(f"emendatusenigmatica:{kind}_gear")
    for kind in unused_materials + ore_processing_gems:
        delete_item(f"emendatusenigmatica:{kind}_clump", f"mekanism:clumps/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_crystal", f"mekanism:crystals/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_dirty_dust", f"mekanism:dirty_dusts/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_shard", f"mekanism:shards/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_fragment", f"bloodmagic:fragments/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_gravel", f"bloodmagic:gravels/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_crushed", f"create:crushed_ores/{kind}")
        delete_item(f"emendatusenigmatica:clean_{kind}", f"mekanism:clean/{kind}")
        delete_item(f"emendatusenigmatica:dirty_{kind}", f"mekanism:dirty/{kind}")
    for kind in unused_materials:
        delete_item(f"emendatusenigmatica:{kind}_ingot", f"forge:ingots/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_block", f"forge:storage_blocks/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_nugget", f"forge:nuggets/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_gem", f"forge:gems/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_dust", f"forge:dusts/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_chunk", f"forge:chunks/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_cluster", f"forge:clusters/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_plate", f"forge:plates/{kind}")
        delete_item(f"emendatusenigmatica:{kind}_rod", f"forge:rods/{kind}")
        delete_item(f"emendatusenigmatica:molten_{kind}", f"forge:molten/{kind}")
        delete_item(f"emendatusenigmatica:molten_{kind}_bucket", f"forge:buckets/{kind}")
    
    # Unify smelting recipies
    for kind in unify_list:
        if "forge:ingots" in has_kind[kind]:
            accum += f"r.unify_ingot({repr(kind)})\n"
    
    # Generate script
    datapack.add_server_script("unify_materials", f"""
        {{
            let r = bind_recipies({repr(preferred)})
            {accum}
        }}
    """)

def write_configs():
    config = datapack.get_toml_config("jaopca/main.toml")
    config["itemSelection"]["preferredMods"] = preference_list

unify_tags()
write_configs()
