// priority: 1000

let hide_events = function(is_hide, hide_list) {
    var doAll = function(f) { hide_list.forEach(f) }
    
    onEvent('jei.hide.items', e => { doAll(x => e.hide(x)) })
    onEvent('jei.hide.fluids', e => { doAll(x => e.hide(x)) })

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

let found_in_events = function(location_list) {
    onEvent('item.tooltip', tooltip => {
        for (var key in location_list) {
            var value = location_list[key]
            tooltip.addAdvanced(key, (item, advanced, text) => {
                text.add(1, `Found in ${value}.`)
            })
        }
    })
}
