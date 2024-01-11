{
    let tome_nbt = '{"eccentrictome:mods":{tconstruct:{0:{id:"tconstruct:materials_and_you",Count:1b},1:{id:"tconstruct:puny_smelting",Count:1b},2:{id:"tconstruct:mighty_smelting",Count:1b},3:{id:"tconstruct:tinkers_gadgetry",Count:1b},4:{id:"tconstruct:fantastic_foundry",Count:1b},5:{id:"tconstruct:encyclopedia",Count:1b}},tetra:{0:{id:"tetra:holo",Count:1b,tag:{"holo/core_material":"frame/dim","holo/frame":"holo/frame","holo/core":"holo/core","holo/frame_material":"core/ancient"}}},astralsorcery:{0:{id:"astralsorcery:tome",Count:1b}},immersiveengineering:{0:{id:"immersiveengineering:manual",Count:1b}},apotheosis:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"apotheosis:apoth_chronicle"}}},eidolon:{0:{id:"eidolon:codex",Count:1b}},iceandfire:{0:{id:"iceandfire:bestiary",Count:1b,tag:{Pages:[I;0]}}},elementalcraft:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"elementalcraft:element_book"}}},solcarrot:{0:{id:"solcarrot:food_book",Count:1b}},botania:{0:{id:"botania:lexicon",Count:1b,tag:{"botania:elven_unlock":1b}}},,ars_nouveau:{0:{id:"ars_nouveau:worn_notebook",Count:1b}},tmechworks:{0:{id:"tmechworks:book",Count:1b}},draconicevolution:{0:{id:"draconicevolution:info_tablet",Count:1b}},bloodmagic:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"bloodmagic:guide"}}},thermal:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"thermal:guidebook"}}},touhou_little_maid:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"touhou_little_maid:memorizable_gensokyo"}}},rftoolsbase:{0:{id:"rftoolsbase:manual",Count:1b}},twilightforest:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"twilightforest:guide"}}},betterendforge:{0:{id:"betterendforge:guidebook",Count:1b}},croptopia:{0:{id:"croptopia:guide",Count:1b}},mysticalagriculture:{0:{id:"patchouli:guide_book",Count:1b,tag:{"patchouli:book":"mysticalagriculture:guide"}}}}}'
    
    onEvent('recipes', event => {
        event.shapeless(Item.of('eccentrictome:tome', tome_nbt), ['minecraft:book', '#forge:bookshelves', 'minecraft:lapis_lazuli'])
    })
    
    let stage_name = "colorfulskies.starting_kit"
    onEvent('player.logged_in', event => {
        if (!event.player.stages.has(stage_name)) {
            console.log(`Granting starting items to ${event.player.toString()}...`);
            event.player.stages.add(stage_name)
            event.player.give(Item.of('eccentrictome:tome', tome_nbt))
        }
    })
}
