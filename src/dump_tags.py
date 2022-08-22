#!/usr/bin/env python3

import os
import os.path
import pack_helper.data
import pack_helper.tags
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
datapack = pack_helper.data.DatapackModel("", "", "")
pack_helper.tags.parse_config(datapack, "tags_reference/blocks.txt", strict = False, no_generate = True, kinds = ["blocks"])
pack_helper.tags.parse_config(datapack, "tags_reference/items.txt", strict = False, no_generate = True, kinds = ["items"])

for tag in sorted(datapack.tags._tags["items"].keys()):
    if sys.argv[1] in tag:
        print(f"#{tag}")
        for item in sorted(datapack.tags._tags["items"][tag]):
            if not "jaopca:" in item:
                print(f"- {item}")
