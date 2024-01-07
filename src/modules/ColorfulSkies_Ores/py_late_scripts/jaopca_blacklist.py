config = datapack.get_toml_config("jaopca/main.toml")

for tag in datapack.tags.list_tags("blocks"):
    if len(datapack.tags.get_tag("blocks", tag)) == 0:
        config["blockTags"]["blacklist"].append(tag)

for tag in datapack.tags.list_tags("items"):
    if len(datapack.tags.get_tag("items", tag)) == 0:
        config["itemTags"]["blacklist"].append(tag)

for tag in datapack.tags.list_tags("fluids"):
    if len(datapack.tags.get_tag("fluids", tag)) == 0:
        config["fluidTags"]["blacklist"].append(tag)
