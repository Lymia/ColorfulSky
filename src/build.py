#!/usr/bin/env python3

import gen.biome_fix
import gen.data
import gen.fix_models
import gen.mod_data
import gen.tags
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
os.makedirs("../kubejs/startup_scripts/generated")

print("- Adding static tags...")
for tag_file in glob.glob('tags/*.txt'):
    gen.tags.parse_config(datapack, tag_file)

print("- Creating Blue Skies tag fix...")
gen.tags.generate_group_redirect(datapack, moddata.unpack_jar(Mod.BlueSkies), "blue_skies", "forge")

print("- Creating Twilight Forest biomes fix...")
gen.biome_fix.fix_biomes(moddata.unpack_jar(Mod.TwilightForest), "../kubejs")

print("- Creating Draconic Evolution resource pack compatibility...")
pack = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
shutil.unpack_archive(find_pack("DP+Pack"), "../build_config/dp", "zip")
gen.fix_models.generate_model_fixes("../build_config/dp", moddata.unpack_jar(Mod.DraconicEvolution), pack)

print("- Generating ores and worldgen configuration...")
import gen.ores
gen.ores.make_ores(datapack, moddata)

print("- Generating misc data...")
datapack.add_i18n("constellation", "itemGroup.constellation", "Constellation")
datapack.add_i18n("constellation", "group.constellation", "Constellation")

print("- Writing configuration...")
gen.data.generate_datapack_files(datapack, "../kubejs/")

print("- Cleaning up...")
shutil.rmtree("../build_config/dp", ignore_errors=True)
