import re
import os
import sys
from typing import Match, Any
import json

GITHUB_OUTPUT = os.environ["GITHUB_OUTPUT"]

bump_version = os.environ.get("NEW_VERSION")

def set_output(name: str, value: Any) -> None:
    with open(GITHUB_OUTPUT, "a", encoding="utf-8") as fp:
        fp.write(f"{name}={value}\n")

with open("Nanolight (Lazer Edition)/skin.ini", encoding="utf-8") as fp:
    try:
        version =re.search(
                pattern=r"^Name: Nanolight Skin (?P<version>(\d|.)+)$",
                string=fp.read(),
                flags=re.MULTILINE,
                ).group(1).split(".")
    except AttributeError:
        print("Couldn't find previous version!")
        sys.exit(1)

if int(os.environ.get("JUST_RETURN_VERSION", 0)):
    set_output("version", ".".join(version))
    sys.exit(0)

if bump_version == "major":
    version[0] = str(int(version[0]) + 1)
    version[1] = "0"
elif bump_version == "minor":
    version[1] = str(int(version[1]) + 1)
else:
    print("Invalid version bump type provided!")
    sys.exit(1)

new_version = ".".join(version)

def repl1(match: Match[str]) -> str:
    global new_version

    return f'Name: Nanolight Skin {new_version}'

with open("Nanolight (Lazer Edition)/skin.ini", encoding="utf-8") as fp:
    new_contents, found = re.subn(
        pattern=r"^Name: Nanolight Skin (?P<version>(\d|.)+)$",
        repl=repl1,
        string=fp.read(),
        count=1,
        flags=re.MULTILINE,
    )

if not found:
    print("Couldn't find 'Name:' line match!")
    sys.exit(1)

def repl2(match: Match[str]) -> str:
    global new_version

    return f'// Version: {new_version}'

new_contents, found = re.subn(
        pattern=r"^// Version: (?P<version>(\d|.)+)$",
        repl=repl2,
        string=new_contents,
        count=1,
        flags=re.MULTILINE,
    )

if not found:
    print("Couldn't find '// Version' line match!")
    sys.exit(1)

with open("Nanolight (Lazer Edition)/skin.ini", "w", encoding="utf-8", newline="\n") as fp:
    fp.write(new_contents)

with open("Nanolight (Lazer Edition)/skininfo.json", encoding="utf-8") as fp:
    skininfo = json.load(fp)

skininfo["Name"] = f"Nanolight Skin {new_version} [Nanolight (Lazer Edition)]"

with open("Nanolight (Lazer Edition)/skininfo.json", "w", encoding="utf-8") as fp:
    json.dump(skininfo, fp, indent=2)

set_output("new_version", new_version)