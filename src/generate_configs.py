#!/usr/bin/env python3

import gen.tags
import glob
import os
import os.path
import shutil

os.chdir(os.path.dirname(os.path.realpath(__file__)))

print("Copying static files...")
shutil.rmtree("../kubejs")
shutil.copytree("static", "../kubejs")

print("Generating tag files...")
tags = gen.tags.TagConfigs()
for tag_file in glob.glob('tags/*.txt'):
    gen.tags.parse_config(tags, tag_file)
gen.tags.generate_tags(tags, "../kubejs/data/")
