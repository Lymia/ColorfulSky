#!/usr/bin/env python3

import os
import os.path
import json
import shutil

current_version = "Alpha 1"

os.chdir(os.path.dirname(os.path.realpath(__file__)))

import build # lazy way!

shutil.rmtree("../build_dist", ignore_errors=True)
os.makedirs("../build_dist")
os.makedirs("../dist", exist_ok=True)

print("Copying files...")
shutil.copytree("../config", "../build_dist/config")
shutil.copytree("../defaultconfigs", "../build_dist/defaultconfigs")
shutil.copytree("../kubejs", "../build_dist/kubejs")
shutil.copytree("../openloader", "../build_dist/openloader")
shutil.copytree("../packmenu", "../build_dist/packmenu")
shutil.copyfile("options.txt", "../build_dist/options.txt")
shutil.copyfile("../README.md", "../build_dist/README.md")

print("Generating manifest...")
manifest = json.loads(open("manifest.json", "r").read())
manifest["name"] = "Colorful Skies"
manifest["author"] = "AuroraAmissa"
manifest["files"].append(
    {'projectID': 411890, 'fileID': 3094111, 'required': True} # Darkpuppey's Modded Overhauls
)
open("../build_dist/manifest.json", "w").write(json.dumps(manifest))

print("Zipping distribution files...")
shutil.make_archive("../dist/Colorful Skies - "+current_version, 'zip', "../build_dist")

print("Cleaning up...")
shutil.rmtree("../build_dist", ignore_errors=True)
