#!/usr/bin/env python3

import gen.biome_fix
import gen.fix_models
import gen.tags
import glob
import os
import os.path
import shutil

from gen.utils import *

print("Generating configuration files...")
shutil.rmtree("../build_config", ignore_errors=True)
os.makedirs("../build_config")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

tags = gen.tags.TagConfigs()

print("- Copying static files...")
shutil.rmtree("../kubejs", ignore_errors=True)
shutil.copytree("static", "../kubejs")
os.makedirs("../kubejs/startup_scripts/generated")

print("- Parsing tag files...")
for tag_file in glob.glob('tags/*.txt'):
    gen.tags.parse_config(tags, tag_file)

print("- Generating Blue Skies fix...")
pack = make_pack("ColorfulSky_BlueSkiesFix", "Colorful Sky - Blue Skies Fix", "data")
shutil.unpack_archive(find_mod("blue_skies"), "../build_config/blueskies", "zip")
os.makedirs(f"{pack}/data/forge/tags")
gen.tags.generate_group_redirect("blue_skies", "forge", "../build_config/blueskies", pack)

print("- Generating Twilight Forest incompatibility fix...")
shutil.unpack_archive(find_mod("twilightforest"), "../build_config/twilightforest", "zip")
gen.biome_fix.fix_biomes("../build_config/twilightforest", "../kubejs")

print("- Generating Draconic Evolution/ProjectE compatibility fix...")
pack = make_pack("DarkpuppeyCompat", "Darkpuppey's Modded Overhauls - 1.16.5 Compatibility Patch", "resources")
shutil.unpack_archive(find_mod("Draconic-Evolution"), "../build_config/de", "zip")
shutil.unpack_archive(find_mod("ProjectE-1.16.5"), "../build_config/pe", "zip")
shutil.unpack_archive(find_pack("DP+Pack"), "../build_config/dp", "zip")
gen.fix_models.generate_model_fixes("../build_config/dp", "../build_config/de", pack)
gen.fix_models.generate_model_fixes("../build_config/dp", "../build_config/pe", pack)

print("- Generating ore-related configuration...")
import gen.ores
open("../kubejs/startup_scripts/generated/worldgen_ores.js", "w").write(gen.ores.make_worldgen())

print("- Generating configuration...")
gen.tags.generate_tags(tags, "../kubejs/data/")

print("- Cleaning up...")
shutil.rmtree("../build_config", ignore_errors=True)
