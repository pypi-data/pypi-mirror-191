from json import loads
from pathlib import Path
from subprocess import run

from .exceptions import SpellerError
from .types import Package


def check_words() -> bool:
    for conf in [
        ".yaspellerrc",
        ".yaspellerrc.js",
        ".yaspellerrc.json",
        ".yaspeller.json",
    ]:
        if Path(conf).exists():
            raise SpellerError(f"YASpeller configuration file found: {conf}")

    package_file = Path("package.json")
    if package_file.exists():
        package: Package = loads(package_file.read_text())
        if "yaspeller" in package:
            raise SpellerError(f"YASpeller configuration file found: {package_file}")

    dictionaries = [
        str(dictionary)
        for dictionary in [Path("personal.json"), Path("wiktionary.json")]
        if dictionary.exists()
    ]

    args = [
        "--check-yo",
        "--find-repeat-words",
        "--report=console,json",
        "--file-extensions=.md",
    ]

    if dictionaries:
        args.append(f"--dictionary={':'.join(dictionaries)}")

    result = run(["npx", "yaspeller", *args, "docs"])
    return bool(result.returncode)
