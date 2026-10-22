"""Explicitly refresh the research dependency lock from the current environment."""
from importlib.metadata import distribution
from pathlib import Path

from packaging.requirements import Requirement


def main():
    seen = {}
    todo = ["numpy", "matplotlib", "jsonschema"]
    while todo:
        package = distribution(todo.pop())
        name = package.metadata["Name"]
        if name.lower() in seen:
            continue
        seen[name.lower()] = (name, package.version)
        for spec in package.requires or []:
            requirement = Requirement(spec)
            if requirement.marker is None or requirement.marker.evaluate({"extra": ""}):
                todo.append(requirement.name)
    path = Path(__file__).resolve().parents[1]/"research/requirements.lock"
    path.write_text(
        "# Exact research dependency closure from the validated Python 3.12 environment.\n"
        + "".join(f"{name}=={version}\n" for name, version in sorted(seen.values())),
        encoding="utf-8",
    )
    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
