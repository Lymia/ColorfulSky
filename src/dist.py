#!/usr/bin/env python3

import cursepy
import os
import os.path
import json
import markdown
import shutil

from gen.utils import *

current_version = "Alpha 1"

os.chdir(os.path.dirname(os.path.realpath(__file__)))

import build # lazy way!

print("Creating modpack distribution file...")
shutil.rmtree("../build_dist", ignore_errors=True)
os.makedirs("../build_dist")
os.makedirs("../dist", exist_ok=True)

print("- Copying files...")
shutil.copytree("../config", "../build_dist/config")
shutil.copytree("../defaultconfigs", "../build_dist/defaultconfigs")
shutil.copytree("../kubejs", "../build_dist/kubejs")
shutil.copytree("../openloader", "../build_dist/openloader")
shutil.copytree("../packmenu", "../build_dist/packmenu")
shutil.copyfile("options.txt", "../build_dist/options.txt")

print("- Generating manifest...")
manifest = json.loads(open("manifest.json", "r").read())
manifest["name"] = "Colorful Skies"
manifest["author"] = "AuroraAmissa"
manifest["files"] += [
    {'projectID': 411890, 'fileID': 3094111, 'required': True}, # Darkpuppey's Modded Overhauls
    {'projectID': 515892, 'fileID': 3427177, 'required': True}, # ProjectE Retexture
    {'projectID': 490095, 'fileID': 3376785, 'required': True}, # Simple CT
]
open("../build_dist/manifest.json", "w").write(json.dumps(manifest))

print("- Generating full modlist...")
curse = cursepy.CurseClient()
modlist_str = ""
for mod in manifest["files"]:
    addon = curse.addon(mod["projectID"])
    print(f"  - {addon.name}")
    modlist_str += f"- [{addon.name}]({addon.url}) ([Download]({addon.url}/files/{mod["fileID"]}))\n"

print("- Rendering markdown...")
open("../build_dist/modlist.html", "w").write(markdown.markdown(modlist_str))
open("../build_dist/readme.html", "w").write(markdown.markdown(open("../README.md").read()))
open("../build_dist/license.html", "w").write(markdown.markdown(open("../LICENSE.md").read()))

print("- Zipping distribution files...")
shutil.make_archive(f"../dist/Colorful Skies - {current_version}", 'zip', "../build_dist")

print("- Cleaning up...")
shutil.rmtree("../build_dist", ignore_errors=True)
