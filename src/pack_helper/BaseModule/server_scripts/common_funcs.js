// priority: 1000

let remove_recipe_by_item, remove_recipe_by_input, remove_recipe_by_output, remove_recipe_by_id, remove_recipe_by_processing_output, run_on_recipes

{
    let recipe_removed_ids = []
    let raw_recipe_removed_outputs = []
    let raw_recipe_removed_inputs = []
    let raw_recipe_removed_processing_outputs = {}
    let recipe_closure = []

    let check_recipe_has_output = function(recipe, list, check_chance) {
        let len = recipe.outputItems.size()
        for (let i = 0; i < len; i++) {
            let stack = recipe.outputItems.get(i)
            if (check_chance && stack.getChance() <= 1.0) continue
            if (list[stack.getId().toString()]) return true
        }
        return false
    }
    let check_recipe_has_input = function(recipe, list) {
        let len = recipe.inputItems.size()
        for (let i = 0; i < len; i++) {
            let stack = recipe.inputItems.get(i)
            if (stack.getId) {
                if (list[stack.getId().toString()]) return true
            } else if (stack.getTag) {
                if (list["#"+stack.getTag()]) return true
            }
        }
        return false
    }

    remove_recipe_by_output = function(value) {
        raw_recipe_removed_outputs.push(value)
    }
    remove_recipe_by_input = function(value) {
        raw_recipe_removed_inputs.push(value)
    }
    remove_recipe_by_item = function(value) {
        remove_recipe_by_output(value)
        remove_recipe_by_input(value)
    }
    remove_recipe_by_id = function(value) {
        recipe_removed_ids[value] = true
    }
    remove_recipe_by_processing_output = function(kind, value) {
        if (!raw_recipe_removed_processing_outputs[kind]) raw_recipe_removed_processing_outputs[kind] = []
        raw_recipe_removed_processing_outputs[kind].push(value)
    }
    run_on_recipes = function(closure) {
        recipe_closure.push(closure)
    }

    onEvent("recipes", e => {
        let recipe_removed_outputs = {}
        let recipe_removed_inputs = {}
        let recipe_removed_processing_outputs = {}
        
        raw_recipe_removed_outputs.forEach(i => 
            ingredient.of(i).stacks.forEach(value => recipe_removed_outputs[value.getId().toString()] = true)
        )
        raw_recipe_removed_inputs.forEach(function(i) {
            if (i.startsWith("#")) recipe_removed_inputs[new String(i)] = true
            ingredient.of(i).stacks.forEach(value => recipe_removed_inputs[value.getId().toString()] = true)
        })
        for (kind in raw_recipe_removed_processing_outputs) {
            recipe_removed_processing_outputs[kind] = {}
            raw_recipe_removed_processing_outputs[kind].forEach(i =>
                ingredient.of(i).stacks.forEach(value => recipe_removed_processing_outputs[kind][value.getId().toString()] = true)
            )
        }
        
        // delete recipes (efficiently)
        console.log("Applying recipe processing...")
        e.forEachRecipeAsync(true, recipe => {
            if (recipe_removed_ids[recipe.getId().toString()]) {
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_output(recipe, recipe_removed_outputs, false)) {
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_input(recipe, recipe_removed_inputs)) {
                recipe.setGroup("constellation:removed")
                return
            }
            
            let process_list = recipe_removed_processing_outputs[recipe.getType()]
            if (process_list && check_recipe_has_output(recipe, process_list, true)) {
                recipe.setGroup("constellation:removed")
                return
            }
        })
        console.log("Recipe processing done!")
        e.remove({ group: "constellation:removed" })
        
        // run custom processing steps
        recipe_closure.forEach(x => x(e))
    })
}

let remove_items = function(remove_list) {
    remove_list.forEach(remove_recipe_by_output)
}
let remove_all_recipes = function(remove_list) {
    remove_list.forEach(remove_recipe_by_item)
}
