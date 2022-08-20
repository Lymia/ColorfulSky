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
    ("rose_quartz", "pink_spinel", "Pink Spinel"), # Conflict with Create
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

def apply_rework(data):
    # Remove unused items
    for gem in silents_gems_unused + silents_gems_used:
        data.remove_name(f"silentgems:{gem}_ore")
        data.remove_name(f"silentgems:{gem}_glowrose")
    for gem in silents_gems_unused:
        data.remove_name(f"silentgems:{gem}_glass")
        data.remove_name(f"silentgems:{gem}_lamp")
        data.remove_name(f"silentgems:{gem}_lamp_inverted_lit")
        data.remove_name(f"silentgems:{gem}_teleporter")
        data.remove_name(f"silentgems:{gem}_redstone_teleporter")
        data.remove_name(f"silentgems:{gem}")
        data.remove_name(f"silentgems:{gem}_shard")
        data.remove_name(f"silentgems:{gem}_return_home_charm")
        data.remove_name(f"silentgems:chaos_{gem}")
        data.remove_name(f"silentgems:{gem}_block")
        data.remove_name(f"silentgems:{gem}_bricks")
    
    # Remove materials for unused items
    for gem in silents_gems_unused + silents_gems_renamed:
        data.add_json_data(f"silentgems/silentgear_materials/{gem}.json", {
            "conditions": [{ "type": "forge:false" }],
            "availability": {},
            "crafting_items": {},
            "name": {
                "translate": "material.silentgear.dummy"
            },
            "stats": {},
            "traits": {},
        })
        
    # Rename materials as needed
    for entry in formal_rename:
        original, new_name, display_name = entry
        
        data.add_i18n("silentgems", f"block.silentgems.{original}_lamp_lit", f"{display_name} Lamp")
        data.add_i18n("silentgems", f"block.silentgems.{original}_lamp_inverted", f"Inverted {display_name} Lamp")
            
        if original != new_name:
            data.add_i18n("silentgems", f"gem.silentgems.{original}", display_name)
            
            # retag gem
            data.tags.add_tag("items", f"silentgems:{original}", f"forge:gems/{new_name}")
            data.tags.add_tag("items", f"#forge:gems/{new_name}", f"forge:gems")
            data.tags.remove_tag("items", f"silentgems:{original}", f"forge:gems/{original}")
            # retag storage block
            data.tags.add_tag(["items", "blocks"], f"silentgems:{original}_block", f"forge:storage_blocks/{new_name}")
            data.tags.add_tag(["items", "blocks"], f"#forge:storage_blocks/{new_name}", f"forge:storage_blocks")
            data.tags.remove_tag(["items", "blocks"], f"silentgems:{original}_block", f"forge:storage_blocks/{original}")
            # retag shard
            data.tags.add_tag("items", f"silentgems:{original}_shard", f"forge:nuggets/{new_name}")
            data.tags.add_tag("items", f"#forge:nuggets/{new_name}", f"forge:nuggets")
            data.tags.remove_tag("items", f"silentgems:{original}_shard", f"forge:nuggets/{original}")
            
    # Add new I18N from new version
    for key in traits_i18n:
        data.add_i18n("silentgems", key, traits_i18n[key])
