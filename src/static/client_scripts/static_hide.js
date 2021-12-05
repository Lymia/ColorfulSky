// Hide misc unused items.
hide_events([])

// Hide unwanted essences from JEI.
events.listen('jei.hide.items', (event) => {
    remove_seed_list.forEach(x => event.hide(`mysticalagriculture:${x}_seeds`))
    remove_seed_list.forEach(x => event.hide(`mysticalagriculture:${x}_essence`))
})

// Hide removed items from JEI.
events.listen('jei.hide.items', (event) => {
    remove_items_list.forEach(x => event.hide(x))
})
