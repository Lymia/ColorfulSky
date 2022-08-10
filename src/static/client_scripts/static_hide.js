// Hide unwanted essences from JEI.
events.listen('jei.hide.items', (event) => {
    remove_seed_list.forEach(x => event.hide(`mysticalagriculture:${x}_seeds`))
    remove_seed_list.forEach(x => event.hide(`mysticalagriculture:${x}_essence`))
})
