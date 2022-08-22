// priority: 1000

let remove_recipe_by_output, remove_recipe_by_id
let run_on_recipies, filter_items

let check_recipe_has_input = function(recipe, list) {
    let len = recipe.inputItems.size()
    for (let i = 0; i < len; i++) {
        let stack = recipe.inputItems.get(i)
        if (list[stack.toString()]) {
            return true
        }
    }
    return false
}
let check_recipe_has_output = function(recipe, list) {
    let len = recipe.outputItems.size()
    for (let i = 0; i < len; i++) {
        let stack = recipe.outputItems.get(i)
        if (list[stack.getId().toString()]) {
            return true
        }
    }
    return false
}

{
    let recipe_removed_ids = {}
    let recipe_removed_outputs = {}
    let recipe_closure = []
    let recipe_remove_closure = {}

    remove_recipe_by_output = function(value) {
        recipe_removed_outputs[value] = true
    }
    remove_recipe_by_id = function(value) {
        recipe_removed_ids[value] = true
    }
    run_on_recipies = function(closure) {
        recipe_closure.push(closure)
    }
    filter_items = function(type, closure) {
        if (!recipe_remove_closure[type]) recipe_remove_closure[type] = []
        recipe_remove_closure[type].push(closure)
    }

    onEvent("recipes", e => {
        // process recipies in one pass
        e.forEachRecipeAsync(true, recipe => {
            // check if the recipe needs to be removed
            if (recipe_removed_ids[recipe.getId().toString()]) {
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_output(recipe, recipe_removed_outputs)) {
                recipe.setGroup("constellation:removed")
                return
            }
            if (recipe_remove_closure[recipe.type.toString()]) {
                let list = recipe_remove_closure[recipe.type.toString()]
                let len = list.length
                for (let i = 0; i < len; i++) {
                    let checker = list[i]
                    if (!checker(recipe)) {
                        console.log("closure " + recipe.getId())
                        recipe.setGroup("constellation:removed")
                        return
                    }
                }
            }
        })
        
        // delete removed recipies
        e.remove({ group: "constellation:removed" })
        
        // run custom processing steps
        recipe_closure.forEach(x => x(e))
    })
}

let remove_items = function(remove_list) {
    remove_list.forEach(remove_recipe_by_output)
}
