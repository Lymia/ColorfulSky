onEvent('worldgen.remove', e => {
    e.removeOres(ore => { ore.blocks = [
        'chisel:marble/raw', 'chisel:limestone/raw', 'chisel:basalt/raw', 'darkerdepths:silver_ore',
    ] })
    e.removeFeatureById("UNDERGROUND_DECORATION", [
        "cavesandcliffs:ore_coal",
        "cavesandcliffs:ore_iron",
        "cavesandcliffs:ore_gold",
        "cavesandcliffs:ore_redstone",
        "cavesandcliffs:ore_diamond",
        "cavesandcliffs:ore_lapis",
    ])
    e.printFeatures()
})
