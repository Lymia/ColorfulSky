// priority: 1000

let hide_events = function(hide_list) {
    var doAll = function(f) { hide_list.forEach(f) }
    onEvent('jei.hide.items', e => { doAll(x => e.hide(x)) }
    onEvent('jei.hide.fluids', e => { doAll(x => e.hide(x)) }
}
