#!/usr/bin/env python3

import glob
import os
import os.path
import pack_helper.biome_fix
import pack_helper.data
import pack_helper.emc_fix
import pack_helper.fix_models
import pack_helper.misc_fixes
import pack_helper.mod_data
import pack_helper.modules
import pack_helper.silents_gems_rework
import pack_helper.tags
import shutil

from pack_helper.utils import *
from pack_helper.mod_data import Mod

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
modules.execute_early()

print("- Copying static files...")
shutil.rmtree("../kubejs", ignore_errors=True)
shutil.copytree("static", "../kubejs")
shutil.rmtree("../kubejs/common_scripts")
for file in glob.glob("static/common_scripts/*.js"):
    shutil.copy(file, "../kubejs/client_scripts")
    shutil.copy(file, "../kubejs/server_scripts")

print("- Loading exported tags...")
pack_helper.tags.parse_config(datapack, "tags_reference/blocks.txt", strict = False, no_generate = True, kinds = ["blocks"])
pack_helper.tags.parse_config(datapack, "tags_reference/items.txt", strict = False, no_generate = True, kinds = ["items"])

print("- Adding static tags...")
for tag_file in glob.glob('tags/*.txt'):
    pack_helper.tags.parse_config(datapack, tag_file)

print("- Creating Twilight Forest biomes fix...")
pack_helper.biome_fix.fix_biomes(moddata.unpack_jar(Mod.TwilightForest), "../kubejs")

print("- Executing Silent's Gems rework...")
pack_helper.silents_gems_rework.apply_rework(datapack)

print("- Creating Draconic Evolution resource pack compatibility...")
pack = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
shutil.unpack_archive(find_pack("DP+Pack"), "run/dp", "zip")
pack_helper.fix_models.generate_model_fixes("run/dp", moddata.unpack_jar(Mod.DraconicEvolution), pack)

print("- Generating EMC configuration...")
pack_helper.emc_fix.make_emc_config()

print("- Applying misc fixes...")
pack_helper.misc_fixes.add_fixes(datapack)

print("- Running modules...")
modules.execute(datapack, moddata)

print("- Generating misc data...")
datapack.add_i18n("constellation", "itemGroup.constellation", "Constellation")
datapack.add_i18n("constellation", "group.constellation", "Constellation")

print("- Writing configuration...")
datapack._finalize()

print("- Cleaning up...")
shutil.rmtree("run/dp", ignore_errors=True)
