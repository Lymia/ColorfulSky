#!/usr/bin/env python3

import gen.data
import gen.tags
import os
import os.path
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
datapack = gen.data.DatapackModel()
gen.tags.parse_config(datapack, "tags_reference/blocks.txt", strict = False, no_generate = True, kinds = ["blocks"])
gen.tags.parse_config(datapack, "tags_reference/items.txt", strict = False, no_generate = True, kinds = ["items"])

for tag in sorted(datapack.tags.tags["items"].keys()):
    if sys.argv[1] in tag:
        print(f"#{tag}")
        for item in sorted(datapack.tags.tags["items"][tag]):
            if not "jaopca:" in item:
                print(f"- {item}")
