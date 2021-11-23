#!/usr/bin/env python3

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

print("- Copying static files...")
shutil.rmtree("../kubejs", ignore_errors=True)
shutil.copytree("static", "../kubejs")

print("- Generating tag files...")
tags = gen.tags.TagConfigs()
for tag_file in glob.glob('tags/*.txt'):
    gen.tags.parse_config(tags, tag_file)
gen.tags.generate_tags(tags, "../kubejs/data/")

print("- Generating Blue Skies fix...")
pack = make_datapack("ColorfulSky_BlueSkiesFix", "Colorful Sky - Blue Skies Fix")
shutil.unpack_archive(find_mod("blue_skies"), "../build_config/blueskies", "zip")
os.makedirs(pack+"/data/forge/tags")
shutil.copytree("../build_config/blueskies/data/blue_skies/tags/blocks", pack+"/data/forge/tags/blocks")
shutil.copytree("../build_config/blueskies/data/blue_skies/tags/items", pack+"/data/forge/tags/items")

print("- Cleaning up...")
shutil.rmtree("../build_config", ignore_errors=True)
