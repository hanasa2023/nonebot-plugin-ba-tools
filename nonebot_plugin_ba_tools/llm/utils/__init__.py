from yaml import Node, SafeDumper


def parse_session_id(session_id: str, type: int):
    pass


def str_presenter(dumper: SafeDumper, data: str) -> Node:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)
