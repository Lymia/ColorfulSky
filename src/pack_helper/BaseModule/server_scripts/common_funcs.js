// priority: 1000

let remove_items = function(remove_list) {
    onEvent("recipes", e => {
        remove_list.forEach(x => e.remove({ output: x }))
    })
}
