// Hide unwanted essences from JEI.
{
    var remove_list = []
    remove_seed_list.forEach(x => {
        remove_list.push(`mysticalagriculture:${x}_seeds`)
        remove_list.push(`mysticalagriculture:${x}_essence`)
    })
    hide_events(false, remove_list)
}
