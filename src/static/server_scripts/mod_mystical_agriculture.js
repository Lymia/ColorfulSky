// Remove all mysticalagriculture essences that represent non-trival materials.
// The modpack is designed to require ProjectE for those instead.

let disable_essence_recipe_list = [
    "astralsorcery/aquamarine",
    "charcoal",
    "refinedstorage/quartz_enriched_iron_ingot",
    "botania/manasteel_ingot",
    "gems/ruby",
    "gems/sapphire",
    "thermal/signalum_ingot",
    "thermal/lumium_ingot",
    "immersiveengineering/hop_graphite_ingot",
    "botania/elementium_ingot",
    "mekanism/osmium_ingot",
    "mekanism/fluorite",
    "mekanism/refined_glowstone_ingot",
    "mekanism/refined_obsidian_ingot",
    "thermal/enderium_ingot",
    "botania/terrasteel_ingot",
    "draconicevolution/draconium_ingot",
];
let replacements_list = [
    ["coal", "fire"], // stone
    ["aquamarine", "water"], // marble
    ["netherite", "wither_skeleton"], // pigstep!!
    ["gold", "blaze"], // pigstep!!
    ["diamond", "starmetal"], // heart of the sea
];

// Remove recipies related to unwanted essences.
onEvent('recipes', e => {
    // Make the seeds uncraftable and remove related recipies
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:seed/infusion/${x}`}))
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:seed/reprocessor/${x}`}))
    // Names that appear often enough that we just throw it at the wall
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:essence/${x}`}))
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:essence/${x}_ingot`}))
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:essence/common/${x}`}))
    remove_seed_list.forEach(x => e.remove({id: `mysticalagriculture:essence/common/${x}_ingot`}))
    // Remove unwanted essence recipies
    disable_essence_recipe_list.forEach(x => e.remove({id: `mysticalagriculture:essence/${x}`}))
    // Replace essences with ones that are still accessible
    replacements_list.forEach(x => e.replaceInput(`mysticalagriculture:${x[0]}_essence`, `mysticalagriculture:${x[1]}_essence`))
})

// TODO: Add new recipies for various mods.

// TODO: Potential hitlist: SGear materials (Sinew, etc)
