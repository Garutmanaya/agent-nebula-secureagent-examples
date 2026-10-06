from __future__ import annotations
import copy, json
from pathlib import Path
def load_presentation(path: Path, data_model: dict) -> dict:
    document=copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))
    document["createSurface"]["dataModel"]=data_model
    return document
