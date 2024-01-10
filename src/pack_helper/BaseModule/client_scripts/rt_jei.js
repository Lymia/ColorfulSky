// priority: 1000

let jei_hide_by_id
let jei_filter_id
{
    let raw_hide_by_id = []
    let filter_by_id = {}
    
    jei_hide_by_id = function(name) {
        raw_hide_by_id.push(name)
    }
    jei_filter_id = function(name, predicate) {
        jei_hide_by_id(name)
        filter_by_id[name] = predicate
    }
    
    let do_hide = function(registry, t, get_id) {
        console.log(`Hiding JEI items for ${registry}`)
        
        let ingredientManager = global.jeiRuntime.getIngredientManager()
        let targetRegistry = undefined
        {
            let list = ingredientManager.getRegisteredIngredientTypes()
            let len = list.size()
            for (let i = 0; i < len; i++) {
                if (list.get(i).getIngredientClass().getName() == registry) {
                    targetRegistry = list.get(i)
                    break
                }
            }
            if (!targetRegistry) throw new Error(`Could not find registry: ${registry}`)
        }
        
        let to_remove = []
        let total_count
        {
            let list = ingredientManager.getAllIngredients(targetRegistry)
            list.forEach(raw_item => {
                let item_id = get_id(raw_item)
                if (t.hide_by_id[item_id]) {
                    let predicate = filter_by_id[item_id]
                    if (predicate && predicate(raw_item)) return;
                    to_remove.push(raw_item)
                }
            })
            total_count = list.size()
        }
        
        if (to_remove.length > 0) ingredientManager.removeIngredientsAtRuntime(targetRegistry, to_remove)
        console.log(`(total: ${total_count}, removed: ${to_remove.length})`)
    }

    onEvent('jei.hide.custom', function(e) {
        let hide_by_id = {}
        raw_hide_by_id.forEach(i => {
            hide_by_id[jstr(i)] = true
            ingredient.of(i).stacks.forEach(value => hide_by_id[jstr(value.getId().toString())] = true)
        })
        
        let t = { hide_by_id: hide_by_id }
        do_hide("net.minecraft.item.ItemStack", t, x => jstr(Ingredient.of(x).getId()))
        do_hide("net.minecraftforge.fluids.FluidStack", t, x => jstr(x.getFluid().getRegistryName().toString()))
        do_hide("mekanism.api.chemical.gas.GasStack", t, x => jstr(x.getTypeRegistryName().toString()))
        do_hide("mekanism.api.chemical.slurry.SlurryStack", t, x => jstr(x.getTypeRegistryName().toString()))
        
        console.log("jei.hide.custom finished")
    })
}

let mark_as_removed
let mark_as_unified
{
    let all_tooltips = []
    
    mark_as_removed = function(name) {
        all_tooltips.push([name, "removed"])
    }
    mark_as_unified = function(name) {
        all_tooltips.push([name, "unified"])
    }
    
    onEvent('item.tooltip', tooltip => {
        all_tooltips.forEach(t => {
            let item = t[0]
            let type = t[1]
            
            if (type == "removed") {
                tooltip.addAdvanced(item, (item, advanced, text) => {
                    text.add(1, "This item has been removed in the Colorful Skies modpack.")
                    text.add(2, "It should not be obtainable.")
                })
            } else if (type == "unified") {
                tooltip.addAdvanced(item, (item, advanced, text) => {
                    text.add(1, "This item has been unified with another in the Colorful Skies modpack.")
                    text.add(2, "It should not be obtainable, and should be automatically converted to another.")
                })
            } else {
                throw new Error("internal error: unknown tooltip type?")
            }
        })
    })
}
