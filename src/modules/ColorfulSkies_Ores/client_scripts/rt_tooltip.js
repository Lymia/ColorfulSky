// priority: 1000

let found_in_events = function(location_list) {
    onEvent('item.tooltip', tooltip => {
        for (let key in location_list) {
            let value = location_list[key]
            tooltip.addAdvanced(key, (item, advanced, text) => {
                text.add(1, `Found in the ${value}.`)
            })
        }
    })
}
