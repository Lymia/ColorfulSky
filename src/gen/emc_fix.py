import json

emc_table = {
    # Adjustments to account for modded worldgen and biomes making some materials cheap.
    "minecraft:gravel": 1,
    "minecraft:flint": 1,
    "#forge:sand": 1,
    "#forge:stone": 1,
    "#forge:end_stones": 1,
    "#forge:netherrack": 1,
    "#mythicbotany:base_stone_alfheim": 1,
    "minecraft:clay": 1, # modded recipies and lush caverns
    "minecraft:clay_ball": 1,
    "minecraft:quartz": 4, # quartz biomes
    "minecraft:glowstone_dust": 4, # glowstone biomes
        
    # Reduce the cost of some items, as Botania can produce them relatively easily
    "minecraft:name_tag": 128,
    "minecraft:apple": 32,
    "minecraft:cocoa_beans": 32,
    "minecraft:soul_sand": 8,
    "minecraft:red_mushroom": 16,
    "minecraft:brown_mushroom": 16,

    # Coral cost shouldn't change when dried, since that allows an exploit.
    "#minecraft:coral_blocks": 32,
    "minecraft:dead_tube_coral_block": 32,
    "minecraft:dead_brain_coral_block": 32,
    "minecraft:dead_bubble_coral_block": 32,
    "minecraft:dead_fire_coral_block": 32,
    "minecraft:dead_horn_coral_block": 32,
    "#minecraft:corals": 16, 
    "minecraft:dead_tube_coral_fan": 16,
    "minecraft:dead_brain_coral_fan": 16,
    "minecraft:dead_bubble_coral_fan": 16,
    "minecraft:dead_fire_coral_fan": 16,
    "minecraft:dead_horn_coral_fan": 16,
    "minecraft:dead_tube_coral": 16,
    "minecraft:dead_brain_coral": 16,
    "minecraft:dead_bubble_coral": 16,
    "minecraft:dead_fire_coral": 16,
    "minecraft:dead_horn_coral": 16,
    
    # Misc fixes to common materials
    "minecraft:bone": 32,
    "minecraft:gunpowder": 32,
    "#forge:dyes": 4,
    "minecraft:prismarine_crystals": 320,
    "minecraft:redstone_block": 576,
    
    # Various foods need updates for farming changes.
    "minecraft:paper": 2,
    "minecraft:enchanted_golden_apple": 64000,
    "#forge:raw_fishes": 64,
    "#forge:cooked_fishes": 64,
    "byg:delphinium": 16,
    
    # Farmer's Delight is a mess EMC-wise
    "farmersdelight:tree_bark": 0,
    "farmersdelight:cabbage_leaf": 16, 
    "farmersdelight:ham": 96,
    "farmersdelight:wild_onions": 36,
    "farmersdelight:brown_mushroom_colony": 80,
    "farmersdelight:red_mushroom_colony": 80,
    "farmersdelight:cod_slice": 30,
    "farmersdelight:cooked_cod_slice": 30,
    "farmersdelight:salmon_slice": 30,
    "farmersdelight:cooked_salmon_slice": 30,
    "farmersdelight:pike_slice": 30,
    "farmersdelight:cooked_pike_slice": 30,
    "farmersdelight:perch_slice": 30,
    "farmersdelight:cooked_perch_slice": 30,
    
    # Botania EMC values
    # We're valuing 1 EMC ~= 25 Mana for this.
    "#botania:petal": 8,
    
    "botania:manasteel_ingot": 250,
    "botania:mana_pearl": 1250,
    "botania:mana_diamond": 8600,
    "botania:terrasteel_ingot": 30000,
    "botania:ender_air_bottle": 256,
    "botania:mana_string": 96, # Slightly less just cus the ratio is so scary otherwise.
    "botania:mana_powder": 24,
    "botania:quartz_mana": 8,
    "botania:mana_glass": 1,
    "mythicbotany:alfsteel_ingot": 90000,
    
    "botania:rune_air": 320,
    "botania:rune_earth": 320, # This is a massive decrease in EMC cost, but it helps consistancy.
    "botania:rune_fire": 320,
    "botania:rune_water": 320,
    "botania:rune_mana": 2750,
    "botania:rune_autumn": 1000,
    "botania:rune_summer": 1000,
    "botania:rune_spring": 1000,
    "botania:rune_winter": 1000,
    "botania:rune_lust": 19000,
    "botania:rune_gluttony": 19000,
    "botania:rune_greed": 19000,
    "botania:rune_sloth": 19000,
    "botania:rune_wrath": 19000,
    "botania:rune_envy": 19000,
    "botania:rune_pride": 19000,
    "extrabotany:elementrune": 320,
    "extrabotany:sinrune": 19000,

    "botania:grass_seeds": 1,
    "botania:podzol_seeds": 1,
    "botania:mycelium_seeds": 1,
    "botania:dry_seeds": 1,
    "botania:golden_seeds": 1,
    "botania:vivid_seeds": 1,
    "botania:scorched_seeds": 1,
    "botania:infused_seeds": 1,
    "botania:mutated_seeds": 1,
    "botania:bifrost_perm": 1,
    "botania:piston_relay": 348,
    "botania:lens_firework": 1500,
    
    "extrabotany:nightmarefuel": 128,
    "extrabotany:friedchicken": 128,
    "extrabotany:aerialite": 30000,
    "extrabotany:heromedal": 30000,
    "extrabotany:orichalcos": 80000,
}

def make_emc_config():
    data = { "entries": [] }
    for entry in emc_table:
        data["entries"].append({ "item": entry, "emc": emc_table[entry] })
    open("../config/ProjectE/custom_emc.json", "w").write(json.dumps(data))
