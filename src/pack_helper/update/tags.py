import cuddle
import glob

class _GatherTags(object):
    def __init__(self):
        # model here is [tag][name] -> set(kinds)
        self._tags = {}

    def push_tag(self, tag, name, kind):
        self._tags.setdefault(tag, {}).setdefault(name, set([])).add(kind)

    def invert_tags(self):
        new = {}
        for tag in self._tags:
            for name in self._tags[tag]:
                str_kinds = ",".join(sorted(list(self._tags[tag][name])))
                target = new.setdefault(tag, {}).setdefault(str_kinds, set([]))
                if name.endswith("?"):
                    if not name[:-1] in target:
                        target.add(name)
                else:
                    if f"{name}?" in target:
                        target.remove(f"{name}?")
                    target.add(name)
        return new

def _parse_kubejs_exported(tags, file_name, kind):
    current_tag = None

    with open(file_name, 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            words = line.split(" ")
            head = words[0]
            args = words[1:]

            if head.startswith('#'):
                current_tag = head[1:]
                continue
            if head == '-':
                assert (current_tag != None)
                name = args[0]
                if name.startswith("jaopca:"):  # hardcoded jaopca ignore
                    continue
                else:
                    tags.push_tag(current_tag, name, kind)
                continue

def _encode_kdl(tags):
    model = tags.invert_tags()
    root_nodes = []

    for tag in sorted(list(model.keys())):
        for kinds in sorted(list(model[tag].keys())):
            nodes = []
            for name in sorted(list(model[tag][kinds])):
                kind = "name"
                properties = {}
                if name.endswith("?"):
                    name = name[:-1]
                    properties["optional"] = True
                if name.startswith("#"):
                    name = name[1:]
                    kind = "tag"
                nodes.append(cuddle.Node(kind, None, properties = properties, arguments = [name]))
            root_nodes.append(cuddle.Node("tag", None, arguments = [tag, kinds], children = nodes))
    return cuddle.dumps(cuddle.Document(cuddle.NodeList(root_nodes)))

def make_tags_from_kubejs():
    tags = _GatherTags()
    for name in glob.glob("../kubejs/exported/tags/*.txt"):
        kind = name.split("/")[-1].split(".")[0]
        _parse_kubejs_exported(tags, name, kind)
    with open("pack/base_content/tags.kdl", "w") as f:
        f.write(_encode_kdl(tags))
