// priority: 1000

let found_in_events = function(location_list) {
    onEvent('item.tooltip', tooltip => {
        for (var key in location_list) {
            var value = location_list[key]
            tooltip.addAdvanced(key, (item, advanced, text) => {
                text.add(1, `Found in the ${value}.`)
            })
        }
    })
}
