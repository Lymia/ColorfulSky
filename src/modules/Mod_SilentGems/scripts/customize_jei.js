// side: client
{
    jei_filter_id("silentgems:soul_gem", item => Ingredient.of(item).getNbt().SGems_SoulGem == "minecraft:zombie")
}

onEvent('item.tooltip', tooltip => {
    let activeGems = [
        "black_diamond", "alexandrite", "turquoise", "heliodor", "iolite",
        "citrine", "peridot", "ammolite", "kyanite", "sapphire", "moldavite",
        "topaz", "carnelian", "ruby", "opal", "rose_quartz",
    ]
    let itemList = []
    activeGems.forEach(x => {
        itemList.push(`silentgems:${x}`)
        itemList.push(`silentgems:${x}_block`)
        itemList.push(`silentgems:${x}_bricks`)
        itemList.push(`silentgems:${x}_glass`)
        itemList.push(`silentgems:${x}_lamp`)
        itemList.push(`silentgems:${x}_lamp_inverted_lit`)
        itemList.push(`silentgems:${x}_teleporter`)
        itemList.push(`silentgems:${x}_redstone_teleporter`)
    })
    itemList.forEach(x => tooltip.addAdvanced(x, (item, advanced, text) => {
        text.remove(1)
    }))
})
