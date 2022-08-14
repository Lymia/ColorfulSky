import glob
import json
import os

def fix_biomes(mod, target):
    for biome in glob.glob(f"{mod}/data/*/worldgen/biome/*.json"):
        target_path = f"{target}{biome[len(mod):]}"
        with open(biome) as fd:
            biome = json.loads(fd.read())
        biome["category"] = "the_end" # huge hack, but...
        os.makedirs(os.path.dirname(target_path), exist_ok = True)
        with open(target_path, "w") as fd:
            fd.write(json.dumps(biome))
