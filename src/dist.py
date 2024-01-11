#!/usr/bin/env python3

# TODO: Compress textures in resource packs

import cursepy
import glob
import os
import os.path
import json
import markdown
import shutil

from pack_helper.utils import *

current_version = "Alpha 1"

os.chdir(os.path.dirname(os.path.realpath(__file__)))
set_release()

import build # lazy way!

print("Creating modpack distribution file...")
shutil.rmtree("../build_dist", ignore_errors=True)
os.makedirs("../build_dist")
os.makedirs("../build_dist/overrides")
os.makedirs("../dist", exist_ok=True)

print("- Removing backup files...")
for path in glob.glob(f"../config/**.bak"):
    os.remove(path)

print("- Copying files...")
shutil.copytree("../config", "../build_dist/overrides/config")
shutil.copytree("../defaultconfigs", "../build_dist/overrides/defaultconfigs")
shutil.copytree("../kubejs", "../build_dist/overrides/kubejs")
shutil.copytree("../openloader", "../build_dist/overrides/openloader")
shutil.copytree("../packmenu", "../build_dist/overrides/packmenu")
shutil.copytree("../tlm_custom_pack", "../build_dist/overrides/tlm_custom_pack") # included for multiplayer reasons
shutil.copyfile("pack/options.txt", "../build_dist/overrides/options.txt")

print("- Removing transient configurations")
delete_file("../build_dist/overrides/config/firstperson.json")
delete_file("../build_dist/overrides/config/oculus.properties")
delete_file("../build_dist/overrides/config/ProjectE/mappingdump.json")
delete_file("../build_dist/overrides/config/startupQoL")
shutil.rmtree("../build_dist/overrides/config/brandon3055/ResourceCache", ignore_errors=True)
shutil.rmtree("../build_dist/overrides/config/brandon3055/ProjectIntelligence", ignore_errors=True)
shutil.rmtree("../build_dist/overrides/config/touhou_little_maid", ignore_errors=True)

print("- Generating manifest...")
manifest = json.loads(open("pack/manifest.json", "r").read())
manifest["name"] = "Colorful Skies"
manifest["version"] = "1.0"
manifest["author"] = "AuroraAmissa"
manifest["files"] += [
    {'projectID': 411890, 'fileID': 3094111, 'required': True}, # Darkpuppey's Modded Overhauls
    {'projectID': 515892, 'fileID': 3427177, 'required': True}, # ProjectE Retexture
    {'projectID': 490095, 'fileID': 3376785, 'required': True}, # Simple CT
    {'projectID': 436186, 'fileID': 3623594, 'required': True}, # Glass Panes CTM Fix
]
open("../build_dist/manifest.json", "w").write(json.dumps(manifest))

print("- Rendering markdown...")
open("../build_dist/readme.html", "w").write(markdown.markdown(open("../README.md").read()))
open("../build_dist/license.html", "w").write(markdown.markdown(open("../LICENSE.md").read()))

print("- Compressing pngs...")
for path in glob.glob(f"../dist/**.png"):
    print(f"- Compressing {path}")
    compress_texture(path)

print("- Zipping distribution files...")
shutil.make_archive(f"../dist/Colorful Skies - {current_version}", 'zip', "../build_dist")

print("- Cleaning up...")
shutil.rmtree("../build_dist", ignore_errors=True)
