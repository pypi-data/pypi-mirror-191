from collections import UserDict
from hashlib import sha1
from pathlib import Path

from yaml import CSafeLoader
from yaml import load

from .exceptions import EventError
from .types import EventName
from .types import Events
from .types import GroupName
from .types import Normalized


def plot_events(check: bool) -> bool:
    data = Path("data")
    events_file = data / "events.yml"

    mermaid = plot(events_file.read_text())

    docs = Path("docs")
    mermaid_file = docs / "events.mmd"

    if check:
        try:
            return mermaid != mermaid_file.read_text()
        except Exception:
            return True
    else:
        docs.mkdir(exist_ok=True)
        mermaid_file.write_text(mermaid)
        return False


def plot(source: str) -> str:
    events: Events = load(source, Loader=CSafeLoader)

    normalized = normalize(events)

    ids = Lookup()

    lines = ["flowchart BT"]

    for group_name, event_list in normalized["groups"].items():
        lines.append(f"  subgraph {group_name}")
        lines.append("    direction BT")
        for event_name in event_list:
            if normalized["definitions"][event_name]:
                left, right = "{{", "}}"
            else:
                left, right = "[", "]"
            lines.append(f"    {ids[event_name]}{left}{event_name}{right}")
        lines.append("  end")
        lines.append("")

    for left, right, decision in normalized["pairs"]:
        sep = f"-- {decision} " if decision is not None else ""
        lines.append(f"  {ids[left]} {sep}--> {ids[right]}")

    for left, right in normalized["causes"]:
        lines.append(f"  {ids[left]} -.-> {ids[right]}")

    return "\n".join(lines) + "\n"


def normalize(events: Events) -> Normalized:
    definitions: dict[EventName, bool] = {}
    groups: dict[GroupName, list[EventName]] = {}
    pairs: list[tuple[EventName, EventName, str | None]] = []
    causes: list[tuple[EventName, EventName]] = []

    for group_name, event_list in events.items():
        group = groups[group_name] = []
        for event_name in event_list:
            if isinstance(event_name, dict):
                name = list(event_name.keys())[0]
                options = list(event_name.values())[0]
                if "previous" not in options:
                    previous = [group[-1]] if group else []
                elif isinstance(options["previous"], str):
                    previous = [options["previous"]]
                elif isinstance(options["previous"], list):
                    previous = options["previous"]
                else:
                    raise RuntimeError
            elif isinstance(event_name, str):
                name = event_name
                options = {}
                previous = [group[-1]] if group else []
            else:
                raise RuntimeError
            if name in definitions:
                raise EventError(f"Duplicated event found: {name}")
            definitions[name] = False
            group.append(name)
            if previous:
                if "decision" in options:
                    if len(previous) > 1:
                        raise EventError(
                            f"Single decision for multiple previous events found: "
                            f"{name}"
                        )
                    for each in previous:
                        definitions[each] = True
                    decision = options["decision"]
                else:
                    decision = None
                for each in previous:
                    pairs.append((each, name, decision))
            if "cause" in options:
                causes.append((options["cause"], name))

    _i: dict[str, dict[str, str]] = {}
    for each, name, decision in pairs:
        if decision is None:
            continue
        _j = _i.setdefault(each, {})
        if decision in _j:
            raise EventError(
                f"Found duplicated decision {decision!r} from event {each!r} "
                f"to {_j[decision]!r} and {name!r}"
            )
        _j[decision] = name

    return {
        "definitions": definitions,
        "groups": groups,
        "pairs": pairs,
        "causes": causes,
    }


class Lookup(UserDict[str, str]):
    def __getitem__(self, item: str) -> str:
        if item in self.data:
            return self.data[item]
        else:
            result = self.data[item] = sha1(item.encode()).hexdigest()
            return result
