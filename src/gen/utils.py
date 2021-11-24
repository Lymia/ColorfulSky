import glob
import os
import os.path
import json
import re
import shutil

def dir_for_texture(tag):
    words = tag.split(":")
    return f"{words[0]}/textures/{words[1]}.png"
def dir_for_tag(tag, kind):
    words = tag.split(":")
    return f"{words[0]}/tags/{kind}/{words[1]}.json"
def find_mod(prefix):
    return glob.glob(f"../mods/{prefix}*.jar")[0]
def find_pack(prefix):
    return glob.glob(f"../resourcepacks/{prefix}*.zip")[0]
def make_pack(name, description, kind):
    path = f"../openloader/{kind}/{name}"
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    if os.path.exists(f"pack_readmes/{name}.md"):
        shutil.copyfile(f"pack_readmes/{name}.md", f"{path}/README.md")
    with open(f"{path}/pack.mcmeta", "w") as fd:
        fd.write(json.dumps({
            "pack": {
                "pack_format": 6,
                "description": description
            }
        }))
    return path
def js_minify_simple(js):
    return re.sub(r"^\s+", "", js, flags=re.MULTILINE)
