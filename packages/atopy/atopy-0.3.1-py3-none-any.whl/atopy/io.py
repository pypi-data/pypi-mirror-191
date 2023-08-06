from json import dump, load
from pathlib import Path
from typing import Any, Optional


def mkdir(path: str) -> None:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)


def json_read(path: str) -> Optional[Any]:
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "rt", encoding="UTF-8") as fp:
        return load(fp)


def json_write(path: str, data: Any, indent: Optional[int] = 4) -> None:
    p = Path(path)
    with open(p, "wt", encoding="UTF-8") as fp:
        dump(data, fp, indent=indent)
