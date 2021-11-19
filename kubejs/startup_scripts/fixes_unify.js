onEvent('recipes', e => {
    function unifyMetalRecipies(name, ingotItem, dustItem, blockItem, nuggetItem) {
        e.replaceInput(nuggetItem, `#forge:nuggets/${name}`)
        e.replaceInput(dustItem, `#forge:dusts/${name}`)
        e.replaceInput(ingotItem, `#forge:ingots/${name}`)
        e.replaceInput(blockItem, `#forge:storage_blocks/${name}`)

        e.replaceOutput(`#forge:ingots/${name}`, ingotItem)
        e.replaceOutput(`#forge:dusts/${name}`, dustItem)
        e.replaceOutput(`#forge:nuggets/${name}`, nuggetItem)
        e.replaceOutput(`#forge:storage_blocks/${name}`, blockItem)
    }
    function unifyMetal(name, ingotItem, dustItem, blockItem, nuggetItem) {
        unifyMetalRecipies(name, ingotItem, dustItem, blockItem, nuggetItem)

        // Remove all existing ore for the metal type.
        e.remove({ input: `#forge:ores/${name}`, type: 'immersiveengineering:crusher' })
        e.remove({ input: `#forge:ingots/${name}`, type: 'immersiveengineering:crusher' })
        e.remove({ input: [`#forge:ores/${name}`, `#forge:dusts/${name}`], output: `#forge:ingots/${name}`, type: 'minecraft:smelting' })
        e.remove({ input: [`#forge:ores/${name}`, `#forge:dusts/${name}`], output: `#forge:ingots/${name}`, type: 'minecraft:blasting' })
        
        // Create new processing recipies for the ingot.
        e.recipes.minecraft.smelting(ingotItem, `#forge:dusts/${name}`).xp(0.5)
        e.recipes.minecraft.blasting(ingotItem, `#forge:dusts/${name}`).xp(0.5)
        e.recipes.immersiveengineering.crusher({ secondaries: [], result: { base_ingredient: { item: dustItem } }, input: { tag: `forge:ingots/${name}` }, energy: 3000 })

        // Create new processing recipies for the ores.
        if (!ingredient.of(`#forge:ores/${name}`).stacks.empty) {
            e.recipes.minecraft.smelting(ingotItem, `#forge:ores/${name}`).xp(1)
            e.recipes.minecraft.blasting(ingotItem, `#forge:ores/${name}`).xp(1)
            e.recipes.mekanism.enriching(item.of(dustItem, 2), `#forge:ores/${name}`)
            e.recipes.immersiveengineering.crusher({
                secondaries: [],
                result: { count: 2, base_ingredient: { item: dustItem } },
                input: { tag: `forge:ores/${name}` },
                energy: 3000
            })
        }
    }
    
    // Unify vanilla (give or take) ores
    unifyMetal('iron', 'minecraft:iron_ingot', 'thermal:iron_dust', 'minecraft:iron_block', 'minecraft:iron_nugget')
    unifyMetal('gold', 'minecraft:gold_ingot', 'thermal:gold_dust', 'minecraft:gold_block', 'minecraft:gold_nugget')
    unifyMetal('copper', 'cavesandcliffs:copper_ingot', 'thermal:copper_dust', 'cavesandcliffs:copper_block', 'cavesandcliffs:copper_nugget')

    // Unify modded ores
    unifyMetal('aluminum', 'immersiveengineering:ingot_aluminum', 'immersiveengineering:dust_aluminum', 'immersiveengineering:block_aluminum', 'immersiveengineering:nugget_aluminum')
    unifyMetal('lead', 'thermal:lead_ingot', 'thermal:lead_dust', 'thermal:lead_block', 'thermal:lead_nugget')
    unifyMetal('nickel', 'thermal:nickel_ingot', 'thermal:nickel_dust', 'thermal:nickel_block', 'thermal:nickel_nugget')
    unifyMetal('silver', 'thermal:silver_ingot', 'thermal:silver_dust', 'thermal:silver_block', 'thermal:silver_nugget')
    unifyMetal('tin', 'thermal:tin_ingot', 'thermal:tin_dust', 'thermal:tin_block', 'thermal:tin_nugget')
    unifyMetal('uranium', 'mekanism:ingot_uranium', 'mekanism:dust_uranium', 'mekanism:block_uranium', 'mekanism:nugget_uranium')

    // Unify alloys
    unifyMetalRecipies('steel', 'mekanism:ingot_steel', 'mekanism:dust_steel', 'mekanism:block_steel', 'mekanism:nugget_steel')
    unifyMetalRecipies('bronze', 'thermal:bronze_ingot', 'thermal:bronze_dust', 'thermal:bronze_block', 'thermal:bronze_nugget')
    unifyMetalRecipies('constantan', 'thermal:constantan_ingot', 'thermal:constantan_dust', 'thermal:constantan_block', 'thermal:constantan_nugget')
    unifyMetalRecipies('electrum', 'thermal:electrum_ingot', 'thermal:electrum_dust', 'thermal:electrum_block', 'thermal:electrum_nugget')
})
