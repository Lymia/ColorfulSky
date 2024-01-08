// priority: 1000

let hide_events = function(is_hide, hide_list) {
    let doAll = function(f) { hide_list.forEach(f) }
    let hideTarget = function(e) {
        hide_list.forEach(id => {
            e.hide(id)
            e.hide(x => {
                console.log(x)
                if (IngredientJS.of(x).getId() == id) return true
                return false
            })
        })
    }
    
    onEvent('jei.hide.items', hideTarget)
    onEvent('jei.hide.fluids', hideTarget)

    if (!is_hide) onEvent('item.tooltip', tooltip => {
        doAll(x => tooltip.addAdvanced(x, (item, advanced, text) => {
            text.add(1, "This item has been removed in the Colorful Skies modpack.")
            text.add(2, "It should not be obtainable.")
        }))
    })
}

let unify_events = function(unify_list) {
    onEvent('item.tooltip', tooltip => {
        unify_list.forEach(x => tooltip.addAdvanced(x, (item, advanced, text) => {
            text.add(1, "This item has been unified with another in the Colorful Skies modpack.")
            text.add(2, "It should not be obtainable, and should be automatically converted to another.")
        }))
    })
}

