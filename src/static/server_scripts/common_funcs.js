// priority: 1000

let bind_recipies = function(e, preferred_list) {
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
        // Unify smelting approaches.
        let ingotItem = find_preferred(`forge:ingots/${kind}`)
        e.remove({ input: [`#forge:ores/${kind}`, `#forge:dusts/${kind}`, `#forge:chunks/${kind}`], output: `#forge:ingots/${kind}`, type: 'minecraft:smelting' })
        e.remove({ input: [`#forge:ores/${kind}`, `#forge:dusts/${kind}`, `#forge:chunks/${kind}`], output: `#forge:ingots/${kind}`, type: 'minecraft:blasting' });
        ["ores", "dusts", "chunks"].forEach(type => {
            if (tag_exists(`forge:${type}/${kind}`)) {
                e.recipes.minecraft.smelting(ingotItem, `#forge:${type}/${kind}`).xp(0.5)
                e.recipes.minecraft.blasting(ingotItem, `#forge:${type}/${kind}`).xp(0.5)
            }
        })
        
        // Unify dust crushing recipies.
        
    }
    let unify_one = function(tag, item) {
        e.replaceInput(`#${tag}`, item)
        e.replaceOutput(`#${tag}`, item)
        ingredient.of(`#${tag}`).stacks.forEach(stack => {
            e.replaceInput(stack.name, item)
            e.replaceOutput(stack.name, item)
        })
    };
    
    for (tag in preferred_list) {
        unify_one(tag, preferred_list[tag])
    }
    
    return {
        unify_ingot: function(kind) {
            unify_smelting(kind)
        },
    }
}
