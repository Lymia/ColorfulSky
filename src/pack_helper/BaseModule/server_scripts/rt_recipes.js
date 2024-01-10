// priority: 1000

let replace_ingredient
let remove_recipe_by_item
let remove_recipe_by_input
let remove_recipe_by_output
let remove_recipe_by_id
let remove_recipe_by_processing_output
let run_on_recipes
{
    let recipe_removed_ids = []
    let raw_replace_ingredient = []
    let raw_recipe_removed_outputs = []
    let raw_recipe_removed_inputs = []
    let raw_recipe_removed_processing_outputs = {}
    let recipe_closure = []
    
    let debug_output = false

    let check_recipe_has_output = function(recipe, list, check_chance) {
        let len = recipe.outputItems.size()
        for (let i = 0; i < len; i++) {
            let stack = recipe.outputItems.get(i)
            if (check_chance && stack.getChance() <= 1.0) continue
            if (list[stack.getId().toString()]) return true
        }
        return false
    }
    let get_ingredient = function(list, stack) {
        if (stack.getId) {
            return list[jstr(stack.getId().toString())]
        } else if (stack.getTag) {
            return list[`#${stack.getTag()}`]
        } else {
            return false
        }
    }
    let check_recipe_has_input = function(recipe, list) {
        let len = recipe.inputItems.size()
        for (let i = 0; i < len; i++) {
            let stack = recipe.inputItems.get(i)
            if (get_ingredient(list, stack)) return true
        }
        return false
    }
    let replace_input = function(recipe, list) {
        let len = recipe.inputItems.size()
        let changed = false
        for (let i = 0; i < len; i++) {
            let stack = recipe.inputItems.get(i)
            let replace_with = get_ingredient(list, stack)
            if (replace_with) {
                recipe.inputItems.set(i, Ingredient.of(replace_with).withCount(stack.getCount()))
                changed = true
            }
        }
        return changed
    }

    replace_ingredient = function(src, dst) {
        raw_replace_ingredient.push([src, dst])
    }
    remove_recipe_by_item = function(value) {
        remove_recipe_by_output(value)
        remove_recipe_by_input(value)
    }
    remove_recipe_by_input = function(value) {
        raw_recipe_removed_inputs.push(value)
    }
    remove_recipe_by_output = function(value) {
        raw_recipe_removed_outputs.push(value)
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
        let recipe_replace_ingredient = {}
        raw_replace_ingredient.forEach(i => {
            let src = i[0]
            let dst = i[1]
            if (src.startsWith("#")) recipe_replace_ingredient[jstr(src)] = dst
            ingredient.of(src).stacks.forEach(value => recipe_replace_ingredient[jstr(value.getId().toString())] = dst)
        })
        
        let recipe_removed_outputs = {}
        raw_recipe_removed_outputs.forEach(i => 
            ingredient.of(i).stacks.forEach(value => recipe_removed_outputs[jstr(value.getId().toString())] = true)
        )
        
        let recipe_removed_inputs = {}
        raw_recipe_removed_inputs.forEach(function(i) {
            if (i.startsWith("#")) recipe_removed_inputs[jstr(new String(i))] = true
            ingredient.of(i).stacks.forEach(value => recipe_removed_inputs[jstr(value.getId().toString())] = true)
        })
        
        let recipe_removed_processing_outputs = {}        
        for (kind in raw_recipe_removed_processing_outputs) {
            recipe_removed_processing_outputs[kind] = {}
            raw_recipe_removed_processing_outputs[kind].forEach(i =>
                ingredient.of(i).stacks.forEach(value => recipe_removed_processing_outputs[kind][jstr(value.getId().toString())] = true)
            )
        }
        
        // delete recipes (efficiently)
        console.log("Applying recipe processing...")
        e.forEachRecipeAsync(true, recipe => {
            let changed = replace_input(recipe, recipe_replace_ingredient)
            
            if (recipe_removed_ids[recipe.getId().toString()]) {
                if (debug_output) console.log(`removed by id: ${recipe}`)
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_output(recipe, recipe_removed_outputs, false)) {
                if (debug_output) console.log(`removed by output: ${recipe}`)
                recipe.setGroup("constellation:removed")
                return
            } else if (check_recipe_has_input(recipe, recipe_removed_inputs)) {
                if (debug_output) console.log(`removed by input: ${recipe}`)
                recipe.setGroup("constellation:removed")
                return
            }
            
            if (changed) {
                recipe.serializeInputs = true
                recipe.save()
            }
            
            let process_list = recipe_removed_processing_outputs[jstr(recipe.getType())]
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

