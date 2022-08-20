import json
import os
import os.path
import shutil
import urllib.request

from enum import Enum
from pack_helper.utils import *

class Mod(Enum):
    Vanilla = 0
    ColorfulSkyOres = 10
    DraconicEvolution = 21
    Create = 22
    Quark = 23
    BYG = 24
    BetterEnd = 25
    DarkerDepths = 26
    TwilightForest = 27
    EmendatusEnigmatica = 28
    InfernalExpansion = 29

mod_prefixes = {
    Mod.DraconicEvolution: "Draconic-Evolution",
    Mod.Create: "create-mc",
    Mod.Quark: "Quark-",
    Mod.BYG: "byg-",
    Mod.BetterEnd: "betterendforge",
    Mod.DarkerDepths: "darkerdepths",
    Mod.TwilightForest: "twilightforest",
    Mod.EmendatusEnigmatica: "EmendatusEnigmatica",
    Mod.InfernalExpansion: "infernal-expansion",
}
fixed_paths = {
    Mod.ColorfulSkyOres: "../openloader/resources/ColorfulSkyOres",
}

def retrieve_minecraft_jar(target):
    if not os.path.exists("run/minecraft.jar"):
        print(f"  - Downloading Minecraft .jar")
        manifest = urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json").read()
        manifest = json.loads(manifest)
        for version in manifest["versions"]:
            if version["id"] == "1.16.5":
                version_manifest = urllib.request.urlopen(version["url"]).read()
                version_manifest = json.loads(version_manifest)
                urllib.request.urlretrieve(version_manifest["downloads"]["client"]["url"], "run/minecraft.jar")
                return "run/minecraft.jar"
        raise Exception("Version 1.16.5 not found.")
    else:
        return "run/minecraft.jar"

class ModData(object):
    unpacked = {}
    
    def __init__(self, target):
        os.makedirs(target, exist_ok = True)
        self.target = target
        
    def find_jar(self, mod):
        if mod == Mod.Vanilla:
            return retrieve_minecraft_jar(self.target)
        else:
            return find_mod(mod_prefixes[mod])
    def unpack_jar(self, mod):
        if mod in fixed_paths:
            return fixed_paths[mod]
        elif mod in self.unpacked:
            return self.unpacked[mod]
        else:
            unpack_dir = f"{self.target}/{mod.name}"
            if not os.path.exists(unpack_dir):
                print(f"  - Unpacking {mod.name} to {unpack_dir}...")
                shutil.unpack_archive(self.find_jar(mod), unpack_dir, "zip")
            self.unpacked[mod] = unpack_dir
            return unpack_dir
        
    def find_path(self, rpath):
        for mod in Mod:
            path = f"{self.unpack_jar(mod)}/{rpath}"
            if os.path.exists(path):
                return path
        raise Exception(f"Path {rpath} not found in any .jar")
    def find_texture(self, name):
        return self.find_path(f"assets/{group(name)}/textures/{path(name)}.png")
