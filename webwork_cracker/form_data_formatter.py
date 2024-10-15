# This file is just to make it a bit faster to format the data used for authentication
import re
import json


def run_formatter():
    print("Formatting...")
    with open("form.html", 'r') as infile:
        to_format = infile.read()

    elements: list[str] = to_format.split('\n')
    out: dict[str, str] = {}
    for e in elements:
        e = e.strip()
        if not e.startswith("<input"):
            continue
        key = re.search("name=\".*?\"", e).group().split('"')[1]
        value = re.search("value=\".*?\"", e).group().split('"')[1]
        out[key] = value

    with open("formatter_output.json", 'w') as outfile:
        json.dump(out, outfile, indent=4)


if __name__ == "__main__":
    run_formatter()

