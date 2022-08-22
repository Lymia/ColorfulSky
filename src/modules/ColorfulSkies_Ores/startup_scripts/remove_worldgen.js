onEvent('worldgen.remove', e => {
    e.removeOres(ore => { ore.blocks = [
        // remove vanilla ores
        "minecraft:coal_ore", "minecraft:iron_ore", "minecraft:gold_ore", "minecraft:diamond_ore",
        "minecraft:redstone_ore", "minecraft:lapis_ore", "minecraft:emerald_ore",
        "minecraft:nether_quartz_ore", "minecraft:nether_gold_ore",
        // remove modded ores
        'darkerdepths:silver_ore',
        'byg:brimstone_nether_gold_ore', 'byg:brimstone_nether_quartz_ore',
        'byg:blue_nether_gold_ore', 'byg:blue_nether_quartz_ore',
        // remove redundant chisel clusters
        'chisel:marble/raw', 'chisel:limestone/raw', 'chisel:basalt/raw',
    ] })
    // remove ender ore
    e.removeFeatureById("UNDERGROUND_ORES", [
        "betterendforge:ender_ore",
    ])
    // remove caves and cliffs mod ores
    e.removeFeatureById("UNDERGROUND_DECORATION", [
        "cavesandcliffs:ore_coal",
        "cavesandcliffs:ore_iron",
        "cavesandcliffs:ore_gold",
        "cavesandcliffs:ore_redstone",
        "cavesandcliffs:ore_diamond",
        "cavesandcliffs:ore_lapis",
    ])
})
