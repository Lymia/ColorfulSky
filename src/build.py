#!/usr/bin/env python3

import glob
import os
import os.path
import pack_helper.data
import pack_helper.fix_models
import pack_helper.gimp
import pack_helper.mod_data
import pack_helper.modules
import pack_helper.tags
import shutil

from pack_helper.utils import *
from pack_helper.mod_data import Mod

print("- Removing old files...")
shutil.rmtree("../kubejs", ignore_errors=True)

print("Generating configuration files...")
if is_release():
    shutil.rmtree("run", ignore_errors=True)
os.makedirs("run", exist_ok = True)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

datapack = pack_helper.data.DatapackModel("../kubejs", "../config", "../openloader")
moddata = pack_helper.mod_data.ModData("run/mods")

print("- Initializing modules...")
modules = pack_helper.modules.ModuleLoader()
modules.execute_init()

print("- Loading exported tags...")
pack_helper.tags.parse_config(datapack, "pack/default_tags/blocks.txt", strict = False, no_generate = True, kinds = ["blocks"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/items.txt", strict = False, no_generate = True, kinds = ["items"], ignore_jaopca = True)
pack_helper.tags.parse_config(datapack, "pack/default_tags/fluids.txt", strict = False, no_generate = True, kinds = ["fluids"], ignore_jaopca = True)

print("- Creating Draconic Evolution resource pack compatibility...")
pack = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
shutil.unpack_archive(find_pack("DP+Pack"), "run/dp", "zip")
pack_helper.fix_models.generate_model_fixes("run/dp", moddata.unpack_jar(Mod.DraconicEvolution), pack)

print("- Running modules...")
modules.execute_early(datapack, moddata)
modules.execute(datapack, moddata)
modules.execute_late(datapack, moddata)

print("- Processing images...")
pack_helper.gimp.reset("run")
gimp = pack_helper.gimp.GimpContext("run")
datapack._finalize_gimp(gimp)

print("- Writing configuration...")
datapack._finalize()

print("- Cleaning up...")
shutil.rmtree("run/dp", ignore_errors=True)
