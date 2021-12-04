// priority: 1000

let bind_gen_ore = function(e) {
    return function(block, parent_stone, cluster_size, cluster_count, min_y, max_y, biomes) {
        if(!Block.getBlock(block)) console.error(`No such block: ${block}`);
        if(parent_stone[0] != "#" && !Block.getBlock(parent_stone)) console.error(`No such block: ${parent_stone}`);
        e.addOre(ore => {
            ore.block = block
            ore.spawnsIn.blacklist = false
            ore.spawnsIn.values = [parent_stone]
            ore.biomes.blacklist = biomes.blacklist
            ore.biomes.values = biomes.values
            ore.clusterMinSize = cluster_size
            ore.clusterMaxSize = cluster_size
            ore.clusterCount = cluster_count
            ore.minHeight = min_y
            ore.maxHeight = max_y
            ore.squared = true
            ore.setWorldgenLayer('top_layer_modification')
        })
    }
}

let bind_gen_blk = function(e) {
    return function(ore_name, hardness, resistance, harvest_tool, harvest_level, material, texture) {
        var block = e.create(ore_name)
        block.material(material).fullBlock(true).texture(texture)
        block.requiresTool(true).hardness(hardness).resistance(resistance).harvestTool(harvest_tool, harvest_level)
    }
}
