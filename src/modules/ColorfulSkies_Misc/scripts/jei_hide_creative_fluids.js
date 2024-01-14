// side: client
{
    jei_filter_id("mekanism:creative_fluid_tank", item => Ingredient.of(item).getNbt() != null)
    jei_filter_id("mekanism:creative_chemical_tank", item => Ingredient.of(item).getNbt() != null)
}
