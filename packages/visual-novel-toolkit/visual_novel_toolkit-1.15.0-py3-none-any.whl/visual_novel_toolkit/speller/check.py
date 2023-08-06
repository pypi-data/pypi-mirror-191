from pathlib import Path
from subprocess import run


def check_words() -> bool:
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
