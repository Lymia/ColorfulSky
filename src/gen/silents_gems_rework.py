silents_gems_unused = [
    "garnet", "topaz", "amber", "heliodor", "peridot", "green_sapphire", "phosphophyllite",
    "aquamarine", "tanzanite", "amethyst", "agate", "morganite", "onyx", "spinel", "jasper",
    "zircon", "malachite", "euclase", "benitoite", "iolite", "lepidolite", "ametrine",
    "moonstone", "pyrope", "coral", "sunstone", "cats_eye", "yellow_diamond", "jade",
    "chrysoprase", "apatite", "fluorite", "sodalite", "kunzite", "tektite", "pearl",
]
silents_gems_used = [
    "black_diamond", "alexanderite", "turquoise", "heliodor", "iolite", "citrine", "peridot",
    "ammolite", "kyanite", "sapphire", "moldavite", "topaz", "carnelian", "ruby",
    "opal", # white diamond in 1.18 version
    "rose_quartz", # replaced with pink sapphire to deal with nasty create overlap
]

def apply_rework(data):
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
