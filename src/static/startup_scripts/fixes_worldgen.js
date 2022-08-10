onEvent('worldgen.remove', e => {
    e.printFeatures()
    e.removeOres(ore => { ore.blocks = [
        'chisel:marble/raw', 'chisel:limestone/raw', 'chisel:basalt/raw', 'darkerdepths:silver_ore',
        'byg:brimstone_nether_gold_ore', 'byg:brimstone_nether_quartz_ore',
        'byg:blue_nether_gold_ore', 'byg:blue_nether_quartz_ore',
    ] })
    e.removeFeatureById("UNDERGROUND_DECORATION", [
        "cavesandcliffs:ore_coal",
        "cavesandcliffs:ore_iron",
        "cavesandcliffs:ore_gold",
        "cavesandcliffs:ore_redstone",
        "cavesandcliffs:ore_diamond",
        "cavesandcliffs:ore_lapis",
    ])
})
