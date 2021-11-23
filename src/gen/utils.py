import glob
import os
import json
import shutil

def dir_for_tag(tag, kind):
    words = tag.split(":")
    return words[0]+"/tags/"+kind+"/"+words[1]+".json"
def find_mod(prefix):
    return glob.glob("../mods/"+prefix+"*.jar")[0]
def make_datapack(name, description):
    path = "../openloader/data/"+name
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    with open(path+"/pack.mcmeta", "w") as fd:
        fd.write(json.dumps({
            "pack": {
                "pack_format": 6,
                "description": description
            }
        }))
    return path
