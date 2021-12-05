onEvent("recipes", e => {
    remove_items_list.forEach(x => e.remove({ output: x }))
})
