// priority: 1000

let remove_recipe_by_output, remove_recipe_by_id, remove_recipe_by_processing_output, run_on_recipies

let check_recipe_has_output = function(recipe, list, check_chance) {
    let len = recipe.outputItems.size()
    for (let i = 0; i < len; i++) {
        let stack = recipe.outputItems.get(i)
        if (check_chance && stack.getChance() <= 1.0) continue
        if (list[stack.getId().toString()]) return true
    }
    return false
}

{
    let recipe_removed_ids = {}
    let recipe_removed_outputs = {}
    let recipe_removed_processing_outputs = {}
    let recipe_closure = []

    remove_recipe_by_output = function(value) {
        ingredient.of(value).stacks.forEach(value => recipe_removed_outputs[value.getId().toString()] = true)
    }
    remove_recipe_by_id = function(value) {
        recipe_removed_ids[value] = true
    }
    remove_recipe_by_processing_output = function(kind, value) {
        if (!recipe_removed_processing_outputs[kind]) recipe_removed_processing_outputs[kind] = {}
        ingredient.of(value).stacks.forEach(value => recipe_removed_processing_outputs[kind][value.getId().toString()] = true)
    }
    run_on_recipies = function(closure) {
        recipe_closure.push(closure)
    }

    onEvent("recipes", e => {
        // delete recipies (efficiently)
        e.forEachRecipeAsync(true, recipe => {
            if (recipe_removed_ids[recipe.getId().toString()]) {
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_output(recipe, recipe_removed_outputs, false)) {
                recipe.setGroup("constellation:removed")
                return
            }
            
            let process_list = recipe_removed_processing_outputs[recipe.getType()]
            if (process_list && check_recipe_has_output(recipe, process_list, true)) {
                console.log("processing "+recipe.getId().toString())
                recipe.setGroup("constellation:removed")
                return
            }
        })
        e.remove({ group: "constellation:removed" })
        
        // run custom processing steps
        recipe_closure.forEach(x => x(e))
    })
}

let remove_items = function(remove_list) {
    remove_list.forEach(remove_recipe_by_output)
}
