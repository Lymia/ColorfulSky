// Remove all mysticalagriculture essences that represent non-trival materials.
// The modpack is designed to require ProjectE for those instead.

let remove_ore_list = [
  "coal",
  "silicon",
  "sulfur",
  "aluminum",
  "copper",
  "apatite",
  "iron",
  "nether_quartz",
  "glowstone",
  "redstone",
  "tin",
  "bronze",
  "zinc",
  "brass",
  "silver",
  "lead",
  "manasteel",
  "aquamarine",
  "quartz_enriched_iron",
  "gold",
  "lapis_lazuli",
  "steel",
  "nickel",
  "constantan",
  "electrum",
  "invar",
  "mithril",
  "tungsten",
  "titanium",
  "uranium",
  "chrome",
  "ruby",
  "sapphire",
  "signalum",
  "lumium",
  "hop_graphite",
  "elementium",
  "osmium",
  "flourite",
  "refined_glowstone",
  "refined_obsidian",
  "diamond",
  "emerald",
  "netherite",
  "platinum",
  "iridium",
  "enderium",
  "terrasteel",
  "draconium",
];
let 
onEvent('recipes', e => {
  remove_ore_list.forEach(x => e.remove({id: `mysticalagriculture:seed/infusion/${x}`}))
})
events.listen('jei.hide.items', (event) => {
  remove_ore_list.forEach(x => event.hide(`mysticalagriculture:${x}_seeds`))
})

// TODO: Make AS marble use water essence instead of aquamarine essence.
