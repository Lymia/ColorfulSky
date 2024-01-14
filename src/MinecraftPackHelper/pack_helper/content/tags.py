import copy
import json

class TagConfig(object):
    def __init__(self):
        self._tags = {}
        self._original_tags = {}

    def store_original(self):
        self._original_tags = copy.deepcopy(self._tags)

    def add_tag(self, kind, name, tag, generated = True):
        if type(kind) == str:
            kind = [kind]
        if type(tag) == str:
            tag = [tag]
        for k in kind:
            for t in tag:
                if generated:
                    if t in self._no_generate:
                        self._no_generate.remove(t)
                self.get_tag(k, t).add(name)
    def remove_tag(self, kind, name, tag, generated = True):
        if type(kind) == str:
            kind = [kind]
        if type(tag) == str:
            tag = [tag]
        for t in tag:
            for k in kind:
                tag_data = self.get_tag(k, t)
                if name in tag_data:
                    if generated:
                        self.force_generate(t)
                    tag_data.remove(name)
    def get_tag(self, kind, tag):
        assert (tag != None)
        return self._tags.setdefault(kind, {}).setdefault(tag, set({}))
    def list_tags(self, kind):
        return list(self._tags[kind].keys())

    def remove_name(self, name):
        for kind_name in self._tags:
            kind = self._tags[kind_name]
            for tag in kind:
                tag_data = kind[tag]
                if name in tag_data:
                    self.force_generate(tag)
                    tag_data.remove(name)
                if f"{name}?" in tag_data:
                    self.force_generate(tag)
                    tag_data.remove(f"{name}?")

    def get_block_tag(self, tag):
        return self.get_tag("blocks", tag)
    def get_item_tag(self, tag):
        return self.get_tag("items", tag)
    def get_fluid_tag(self, tag):
        return self.get_tag("fluids", tag)
    def get_slurry_tag(self, tag):
        return self.get_tag("slurries", tag)
    def get_gas_tag(self, tag):
        return self.get_tag("gases", tag)

    def add_block_tag(self, name, tag):
        self.add_tag("blocks", name, tag)
    def add_item_tag(self, name, tag):
        self.add_tag("items", name, tag)
    def add_both_tag(self, name, tag):
        self.add_tag(["blocks", "items"], name, tag)
