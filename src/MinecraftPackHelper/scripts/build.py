import os
import pack_helper.data
import pack_helper.gimp
import pack_helper.mod_data
import pack_helper.modules
import pack_helper.tags
import shutil

from pack_helper.utils import *

os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/../..")

print("- Removing old files...")
shutil.rmtree("../kubejs", ignore_errors = True)

print("Generating configuration files...")
if is_release():
    shutil.rmtree("run", ignore_errors = True)
os.makedirs("run", exist_ok = True)

datapack = pack_helper.data.DatapackModel("../kubejs", "../config", "../openloader")

print("- Indexing mod files...")
moddata = pack_helper.mod_data.ModData()

print("- Initializing modules...")
modules = pack_helper.modules.ModuleLoader()
modules.execute_init(datapack, moddata)

print("- Loading exported tags...")
pack_helper.tags.parse_config(datapack, "pack/default_tags/blocks.txt", strict = False, no_generate = True,
                              kinds = ["blocks"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/items.txt", strict = False, no_generate = True,
                              kinds = ["items"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/fluids.txt", strict = False, no_generate = True,
                              kinds = ["fluids"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/gases.txt", strict = False, no_generate = True,
                              kinds = ["gases"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/slurries.txt", strict = False, no_generate = True,
                              kinds = ["slurries"], ignore_jaopca = True)
datapack.tags.store_original()

print("- Running modules...")
modules.execute_early(datapack, moddata)
modules.execute(datapack, moddata)
modules.execute_late(datapack, moddata)

print("- Processing images...")
pack_helper.gimp.reset()
gimp = pack_helper.gimp.GimpContext()
datapack._finalize_gimp(gimp)

print("- Writing configuration...")
datapack._finalize()
