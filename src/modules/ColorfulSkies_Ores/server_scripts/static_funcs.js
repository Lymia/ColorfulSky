// priority: 1000

// TODO: Rewrite this to use the faster recipe system.

let bind_recipies = function(preferred_list) {
    let find_preferred = function(tag) {
        if (!preferred_list[tag]) {
            let ingredients = ingredient.of(`#${tag}`).stacks
            if (ingredients.empty) throw `No ingredients found for tag ${tag}.`
            let targetIngredients = ingredients.find(x => x.startsWith("jaopca:"))
            if (!targetIngredients) {
                console.warn(`No preferred item found for ${tag}. Defaulting to: ${ingredients.first.name}`)
                targetIngredients = ingredients.first
            }
            preferred_list[tag] = targetIngredients
            return targetIngredients
        } else {
            return preferred_list[tag]
        }
    }
    
    let tag_exists = function(tag) {
        return !ingredient.of(`#${tag}`).stacks.empty
    }
    let unify_smelting = function(kind) {        
        let ingotItem = find_preferred(`forge:ingots/${kind}`)

        // Unify smelting recipes
        remove_recipe_by_processing_output("minecraft:smelting", `#forge:ingots/${kind}`)
        remove_recipe_by_processing_output("minecraft:blasting", `#forge:ingots/${kind}`)
        run_on_recipes(e => {
            ["ores", "dusts", "chunks"].forEach(type => {
                if (tag_exists(`forge:${type}/${kind}`)) {
                    e.recipes.minecraft.smelting(ingotItem, `#forge:${type}/${kind}`).xp(0.5)
                    e.recipes.minecraft.blasting(ingotItem, `#forge:${type}/${kind}`).xp(0.5)
                }
            })
        })
        
        // Unify dust crushing recipies.
        // TODO
    }
    let unify_one = function(tag, item) {
        run_on_recipes(e => {
            e.replaceInput(`#${tag}`, item)
            ingredient.of(`#${tag}`).stacks.forEach(stack => {
                e.replaceInput(stack.getId(), item)
                e.replaceOutput(stack.getId(), item)
            })
        })
    }
    
    for (tag in preferred_list) {
        unify_one(tag, preferred_list[tag])
    }
    
    return {
        unify_ingot: function(kind) {
            unify_smelting(kind)
        },
    }
}
