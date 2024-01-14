// priority: 1000
// side: startup

let add_gen_ore

{
    let ore_data_list = []
    let is_scrambled = false

    add_gen_ore = function(block, parent_stone, cluster_size, cluster_count, min_y, max_y, biomes) {
        if(!Block.getBlock(block)) console.error(`No such block: ${block}`);
        if(parent_stone[0] != "#" && !Block.getBlock(parent_stone)) console.error(`No such block: ${parent_stone}`);
        
        for (let i = 0; i < cluster_count; i++) { // Workaround for a horrible bug.
            ore_data_list.push({
                "block": block,
                "parent_stone": parent_stone,
                "cluster_size": cluster_size,
                "min_y": min_y,
                "max_y": max_y,
                "biomes": biomes,
            })
        }
    }

    onEvent('worldgen.add', e => {
        if (!is_scrambled) {
            console.log("Scrambling worldgen data list...")
                    
            is_scrambled = true
            
            // scramble the oregen list to help it be less predictable
            let rng = 2856674
            for (let i = 0; i < ore_data_list.length; i++) {
                let j = i + ((rng >> 20) % (ore_data_list.length - i))
                if (i != j) {
                    let tmp = ore_data_list[i]
                    ore_data_list[i] = ore_data_list[j]
                    ore_data_list[j] = tmp
                }
                rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF;
            }
            console.log(`Total ${ore_data_list.length} ore generators made. :(`)
            console.log("(stupid bug workarouds...)")
        }
        
        for (let idx in ore_data_list) {
            let data = ore_data_list[idx]
            e.addOre(ore => {
                ore.block = data.block
                ore.spawnsIn.blacklist = false
                ore.spawnsIn.values = [data.parent_stone]
                ore.biomes.blacklist = data.biomes.blacklist
                ore.biomes.values = data.biomes.values
                ore.clusterMaxSize = data.cluster_size
                ore.clusterCount = 1
                ore.minHeight = data.min_y
                ore.maxHeight = data.max_y
                ore.squared = true
                ore.noSurface = false
                ore.worldgenLayer = 'top_layer_modification'
            })
        }
    })
}

let bind_gen_blk = function(e) {
    return function(ore_name, display_name, hardness, resistance, harvest_tool, harvest_level, material, texture) {
        let block = e.create(ore_name)
        block.material(material).fullBlock(true).textureAll(texture).displayName(display_name)
        block.requiresTool(true).hardness(hardness).resistance(resistance).harvestTool(harvest_tool, harvest_level)
    }
}
