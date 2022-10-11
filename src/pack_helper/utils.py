import glob
import os
import os.path
import json
import pngquant
import re
import shutil
import zopfli

from PIL import Image

def delete_file(f):
    if os.path.exists(f):
        os.remove(f)

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
def js_minify_simple(js, priority = 0):
    js = re.sub(r" +", " ", js, flags=re.MULTILINE)
    js = re.sub(r"^\s+", "", js, flags=re.MULTILINE)
    js = re.sub(r"\n+", "\n", js, flags=re.MULTILINE)
    js = re.sub(r",\s+", ",", js, flags=re.MULTILINE)
    js = re.sub(r":\s+", ":", js, flags=re.MULTILINE)
    js = re.sub(r"\(\s+", "(", js, flags=re.MULTILINE)
    js = re.sub(r"\s+\)", ")", js, flags=re.MULTILINE)
    return f"// priority: {priority}\n// Generated by Colorful Skies build script. Do not edit directly.\n{js}"

def make_parents(path):
    os.makedirs(os.path.dirname(path), exist_ok = True)
def open_mkdir(path, mode = "w"):
    make_parents(path)
    return open(path, mode)

def group(name):
    return name.split(":", 1)[0]
def path(name):
    return name.split(":", 1)[1]

def short_tag(tag):
    if ":" in tag:
        return tag
    else:
        return f"forge:{tag}"

zopflipng = zopfli.ZopfliPNG()
def compress_texture(target_path):
    pngquant.quant_image(target_path)
    with open(target_path, "rb") as fd:
        image_data = zopflipng.optimize(fd.read())
    with open(target_path, "wb") as fd:
        fd.write(image_data)

INTERNAL_FLAG_IS_RELEASE = False
def is_release():
    return INTERNAL_FLAG_IS_RELEASE
def set_release():
    global INTERNAL_FLAG_IS_RELEASE
    INTERNAL_FLAG_IS_RELEASE = True
