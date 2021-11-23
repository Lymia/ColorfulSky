onEvent('worldgen.remove', e => {
    e.removeOres(ore => { ore.blocks = [
        'chisel:marble/raw', 'chisel:limestone/raw', 'chisel:basalt/raw', "darkerdepths:silver_ore"
    ] })
})
