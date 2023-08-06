import re


def parse_tag(line):
    line_ = line
    if "#" in line_:
        line_, *_ = line_.split("#")

    if "!" in line_:
        line_, *_ = line_.split("!")

    if "=" not in line_:
        return None

    tag, val = [e.strip() for e in line_.split("=")]

    return (tag, val)


def get_value(source, tag, default, cast=float):
    for line in source:
        res = parse_tag(line)
        if res and res[0] == tag:
            return cast(res[1])

    return default


def parse_incar(source, tags):
    with open(source) as f:
        lines = f.readlines()

    values = {}

    for tag, params in tags.items():
        values[tag] = get_value(lines, tag, **params)

    return values
