remove_seed_list = [
    "coal",
    "rubber",
    "silicon",
    "sulfur",
    "aluminum",
    "copper",
    "apatite",
    "iron",
    "redstone",
    "tin",
    "bronze",
    "zinc",
    "brass",
    "silver",
    "lead",
    "manasteel",
    "aquamarine",
    "quartz_enriched_iron",
    "gold",
    "lapis_lazuli",
    "steel",
    "nickel",
    "constantan",
    "electrum",
    "invar",
    "mithril",
    "tungsten",
    "titanium",
    "uranium",
    "chrome",
    "ruby",
    "sapphire",
    "signalum",
    "lumium",
    "hop_graphite",
    "elementium",
    "osmium",
    "flourite",
    "refined_glowstone",
    "refined_obsidian",
    "diamond",
    "emerald",
    "netherite",
    "platinum",
    "iridium",
    "enderium",
    "terrasteel",
    "draconium",
    "firey_ingot",
    "steeleaf",
    "knightmetal",
    "hepatizon",
    "queens_slime",
    "manyullyn",
    "rose_gold",
    "cobalt",
    "ender_biotite",
    "graphite",
    "slimesteel",
    "pig_iron",
    "tinkers_bronze",
]
replacements_list = [
    ("coal", "fire"), # stone
    ("aquamarine", "water"), # marble
    ("netherite", "wither_skeleton"), # pigstep!!
    ("gold", "blaze"), # pigstep!!
    ("diamond", "starmetal"), # heart of the sea
]

for seed in remove_seed_list:
    datapack.remove_name(f"mysticalagriculture:{seed}_seeds")
    datapack.remove_name(f"mysticalagriculture:{seed}_essence")
for entry in replacements_list:
    src, dst = entry
    datapack.replace_ingredient(f"mysticalagriculture:{src}_essence", f"mysticalagriculture:{dst}_essence")
