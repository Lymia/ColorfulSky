import fnmatch
import glob
import json
import os
import urllib.request
import zipfile

from pack_helper.utils import group,path

def _retrieve_minecraft_jar():
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

class _ZipDataIndex(object):
    def __init__(self):
        self._zip_files = []
        self._index = {}

    def add_jar(self, jar):
        idx = len(self._zip_files)
        zip_file = zipfile.ZipFile(jar)

        self._zip_files.append(zip_file)
        for name in zip_file.namelist():
            if not name in self._index:
                self._index[name] = idx

    def read(self, path):
        zip_file = self._zip_files[self._index[path]]
        return zip_file.read(path)

    def glob(self, pattern):
        return list(filter(lambda x: fnmatch.fnmatchcase(x, pattern), self._index.keys()))

def _load_jars():
    idx = _ZipDataIndex()
    idx.add_jar(_retrieve_minecraft_jar())
    for path in glob.glob("../mods/*.jar"):
        idx.add_jar(path)
    return idx

class ModData(object):
    unpacked = {}

    def __init__(self):
        os.makedirs("run/extracted", exist_ok = True)
        self._extracted_id = 0
        self._idx = _load_jars()
        self._extract_cache = {}

    def find_path(self, path):
        if not path in self._extract_cache:
            self._extracted_id = self._extracted_id + 1
            id = self._extracted_id
            name = path.split("/")[-1]
            target_path = f"run/extracted/{id}_{name}"
            with open(target_path, "wb") as fd:
                fd.write(self._idx.read(path))
            self._extract_cache[path] = target_path
            return target_path
        else:
            return self._extract_cache[path]

    def find_asset(self, path):
        return self.find_path(f"assets/{path}")
    def find_texture(self, name):
        return self.find_path(f"assets/{group(name)}/textures/{path(name)}.png")

    def read_path(self, path):
        return self._idx.read(path)
    def read_asset(self, path):
        return self._idx.read(f"assets/{path}")

    def glob(self, pattern):
        return self._idx.glob(pattern)
