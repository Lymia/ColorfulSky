silents_gems_unused = [
    "garnet", "amber", "green_sapphire", "phosphophyllite", "aquamarine", "tanzanite",
    "amethyst", "agate", "morganite", "onyx", "spinel", "jasper", "zircon", "malachite",
    "euclase", "benitoite", "lepidolite", "ametrine", "moonstone", "pyrope", "coral",
    "sunstone", "cats_eye", "yellow_diamond", "jade", "chrysoprase", "apatite", "fluorite",
    "sodalite", "kunzite", "tektite", "pearl",
]
silents_gems_used = [
    "black_diamond", "alexandrite", "turquoise", "heliodor", "iolite", "citrine", "peridot",
    "ammolite", "kyanite", "sapphire", "moldavite", "topaz", "carnelian", "ruby",
    "opal", "rose_quartz",
]
silents_gems_renamed = [
    "opal", "rose_quartz",
]
formal_rename = [
    ("black_diamond", "black_diamond", "Black Diamond"),
    ("alexandrite", "alexandrite", "Alexandrite"),
    ("turquoise", "turquoise", "Turquoise"),
    ("heliodor", "heliodor", "Heliodor"),
    ("iolite", "iolite", "Iolite"),
    ("citrine", "citrine", "Citrine"),
    ("peridot", "peridot", "Peridot"),
    ("ammolite", "ammolite", "Ammolite"),
    ("kyanite", "kyanite", "Kyanite"),
    ("sapphire", "sapphire", "Sapphire"),
    ("moldavite", "moldavite", "Moldavite"),
    ("topaz", "topaz", "Topaz"),
    ("carnelian", "carnelian", "Carnelian"),
    ("ruby", "ruby", "Ruby"),
    ("opal", "white_diamond", "White Diamond"), # Renamed in 1.17+
    ("rose_quartz", "rhodonite", "Rhodonite"), # Conflict with Create
]
override_graphics = [
    ("alexandrite", "amethyst"),
    ("ammolite", "agate"),
    ("carnelian", "garnet"),
    ("citrine", "amber"),
    ("iolite", "tanzanite"),
    ("kyanite", "fluorite"),
    ("moldavite", "peridot"),
    ("peridot", "green_sapphire"),
    ("rose_quartz", "pyrope"),
    ("turquoise", "apatite"),
]
traits_i18n = {
    "trait.silentgems.barrier_jacket": "Barrier Jacket",
    "trait.silentgems.barrier_jacket.desc": "Grants more magic armor at higher durability",
    "trait.silentgems.booster": "Booster",
    "trait.silentgems.booster.desc": "Gives a speed boost",
    "trait.silentgems.cloaking": "Cloaking",
    "trait.silentgems.cloaking.desc": "Grants invisibility",
    "trait.silentgems.fractal": "Fractal",
    "trait.silentgems.fractal.desc": "Gains armor toughness, but loses magic armor as damaged",
    "trait.silentgems.hearty": "Hearty",
    "trait.silentgems.hearty.desc": "Gives extra health",
    "trait.silentgems.leaping": "Leaping",
    "trait.silentgems.leaping.desc": "Gives jump boost and slow falling",
    # Name update
    "trait.silentgems.critical": "Critical Strike",
    "trait.silentgems.critical.desc": "Sometimes deals significantly more damage than normal",
}

def apply_rework():
    # Remove unused items
    datapack.remove_name("silentgems:glowrose_basket")
    datapack.remove_name("silentgems:glowrose_fertilizer")
    datapack.remove_name("silentgems:slime_crystal")
    datapack.remove_name("silentgems:ender_slime_crystal")
    for gem in silents_gems_unused + silents_gems_used:
        datapack.remove_name(f"silentgems:{gem}_ore")
        datapack.remove_name(f"silentgems:{gem}_glowrose")
        datapack.remove_name(f"silentgems:{gem}_shard")
        datapack.remove_recipe(f"silentgems:altar_transmutation/gem/{gem}")
    for gem in silents_gems_unused:
        datapack.remove_name(f"silentgems:{gem}_glass")
        datapack.remove_name(f"silentgems:{gem}_lamp")
        datapack.remove_name(f"silentgems:{gem}_lamp_inverted_lit")
        datapack.remove_name(f"silentgems:{gem}_teleporter")
        datapack.remove_name(f"silentgems:{gem}_redstone_teleporter")
        datapack.remove_name(f"silentgems:{gem}")
        datapack.remove_name(f"silentgems:{gem}_return_home_charm")
        datapack.remove_name(f"silentgems:chaos_{gem}")
        datapack.remove_name(f"silentgems:{gem}_block")
        datapack.remove_name(f"silentgems:{gem}_bricks")
    
    # Remove materials for unused items
    for gem in silents_gems_unused + silents_gems_renamed:
        datapack.add_json_data(f"silentgems/silentgear_materials/{gem}.json", {
            "conditions": [{ "type": "forge:false" }],
            "availability": {},
            "crafting_items": {},
            "name": {
                "translate": "material.silentgear.dummy"
            },
            "stats": {},
            "traits": {},
        })
        
    # Rename materials and modify game data as needed
    for entry in formal_rename:
        original, new_name, display_name = entry
        
        datapack.add_i18n("silentgems", f"block.silentgems.{original}_lamp_lit", f"{display_name} Lamp")
        datapack.add_i18n("silentgems", f"block.silentgems.{original}_lamp_inverted", f"Inverted {display_name} Lamp")
        
        if original != new_name:
            datapack.add_i18n("silentgems", f"gem.silentgems.{original}", display_name)
            
            # retag gem
            datapack.tags.add_tag("items", f"silentgems:{original}", f"forge:gems/{new_name}")
            datapack.tags.add_tag("items", f"#forge:gems/{new_name}", f"forge:gems")
            datapack.tags.remove_tag("items", f"silentgems:{original}", f"forge:gems/{original}")
            # retag storage block
            datapack.tags.add_tag(["items", "blocks"], f"silentgems:{original}_block", f"forge:storage_blocks/{new_name}")
            datapack.tags.add_tag(["items", "blocks"], f"#forge:storage_blocks/{new_name}", f"forge:storage_blocks")
            datapack.tags.remove_tag(["items", "blocks"], f"silentgems:{original}_block", f"forge:storage_blocks/{original}")
            # retag shard
            datapack.tags.add_tag("items", f"silentgems:{original}_shard", f"forge:nuggets/{new_name}")
            datapack.tags.add_tag("items", f"#forge:nuggets/{new_name}", f"forge:nuggets")
            datapack.tags.remove_tag("items", f"silentgems:{original}_shard", f"forge:nuggets/{original}")
    
    # Create recipies for renamed entries
    for entry in formal_rename:
        original, new_name, display_name = entry
        
        datapack.add_json_data(f"silentgems/recipes/bricks/{original}.json", {
            "type": "minecraft:crafting_shaped",
            "group": "classic_gem_bricks",
            "pattern": [
                "###",
                "#g#",
                "###"
            ],
            "key": {
                "g": {
                "tag": f"forge:gem/{new_name}"
                },
                "#": {
                "item": "minecraft:stone_bricks"
                }
            },
            "result": {
                "item": f"silentgems:{original}_bricks",
                "count": 12
            }
        })
        datapack.add_json_data(f"silentgems/recipes/glass/{original}.json", {
            "type": "minecraft:crafting_shaped",
            "group": "classic_gem_glass",
            "pattern": [
                "###",
                "#g#",
                "###"
            ],
            "key": {
                "g": {
                "tag": f"forge:gem/{new_name}"
                },
                "#": {
                "item": "minecraft:glass"
                }
            },
            "result": {
                "item": f"silentgems:{original}_glass",
                "count": 12
            }
        })
            
    # Copy assets to fix coloring
    for entry in override_graphics:
        dst, src = entry
        datapack.copy_asset(f"silentgems/textures/block/gem/{dst}_block.png", moddata.find_asset(f"silentgems/textures/block/gem/{src}_block.png"))
        datapack.copy_asset(f"silentgems/textures/block/glass/{dst}.png", moddata.find_asset(f"silentgems/textures/block/glass/{src}.png") )
        datapack.copy_asset(f"silentgems/textures/block/teleporter/redstone/{dst}.png", moddata.find_asset(f"silentgems/textures/block/teleporter/redstone/{src}.png"))
        datapack.copy_asset(f"silentgems/textures/block/teleporter/standard/{dst}.png", moddata.find_asset(f"silentgems/textures/block/teleporter/standard/{src}.png"))
        datapack.copy_asset(f"silentgems/textures/item/chaos_gem/{dst}.png", moddata.find_asset(f"silentgems/textures/item/chaos_gem/{src}.png"))
        datapack.copy_asset(f"silentgems/textures/models/armor/{dst}_layer_1.png", moddata.find_asset(f"silentgems/textures/models/armor/{src}_layer_1.png"))
        datapack.copy_asset(f"silentgems/textures/models/armor/{dst}_layer_2.png", moddata.find_asset(f"silentgems/textures/models/armor/{src}_layer_2.png"))
           
    # Add new I18N from new version
    for key in traits_i18n:
        datapack.add_i18n("silentgems", key, traits_i18n[key])

apply_rework()
