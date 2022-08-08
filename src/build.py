#!/usr/bin/env python3

import gen.biome_fix
import gen.data
import gen.emc_fix
import gen.fix_models
import gen.mod_data
import gen.ores
import gen.tags
import gen.unify
import glob
import os
import os.path
import shutil

from gen.utils import *
from gen.mod_data import Mod

print("Generating configuration files...")
if is_release():
    shutil.rmtree("../build_config", ignore_errors=True)
os.makedirs("../build_config", exist_ok = True)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

datapack = gen.data.DatapackModel()
moddata = gen.mod_data.ModData("../build_config/mods")

print("- Copying static files...")
shutil.rmtree("../kubejs", ignore_errors=True)
shutil.copytree("static", "../kubejs")
shutil.rmtree("../kubejs/common_scripts")
for file in glob.glob("static/common_scripts/*.js"):
    shutil.copy(file, "../kubejs/client_scripts")
    shutil.copy(file, "../kubejs/server_scripts")

print("- Adding static tags...")
for tag_file in glob.glob('tags/*.txt'):
    gen.tags.parse_config(datapack, tag_file)

print("- Creating Twilight Forest biomes fix...")
gen.biome_fix.fix_biomes(moddata.unpack_jar(Mod.TwilightForest), "../kubejs")

print("- Creating Draconic Evolution resource pack compatibility...")
pack = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
shutil.unpack_archive(find_pack("DP+Pack"), "../build_config/dp", "zip")
gen.fix_models.generate_model_fixes("../build_config/dp", moddata.unpack_jar(Mod.DraconicEvolution), pack)

print("- Generating ores and worldgen configuration...")
gen.ores.make_ores(datapack, moddata)

print("- Generating EMC configuration...")
gen.emc_fix.make_emc_config()

print("- Unifying materials...")
gen.unify.unify_tags(datapack)
gen.unify.write_configs()

print("- Generating misc data...")
datapack.add_i18n("constellation", "itemGroup.constellation", "Constellation")
datapack.add_i18n("constellation", "group.constellation", "Constellation")

print("- Writing configuration...")
gen.data.generate_datapack_files(datapack, "../kubejs/")

print("- Cleaning up...")
shutil.rmtree("../build_config/dp", ignore_errors=True)
