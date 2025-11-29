
import json


_SCHEMA_PATH = "object_schema.json"
with open(_SCHEMA_PATH) as f:
    _SCHEMA = json.load(f)

def _parse_schema(schema: dict) -> tuple[dict, dict, dict]:
    level_to_object = {}
    object_to_level = {}
    level_to_level = {}

    for level_name, level in schema["levels"].items():
        level_to_object[level_name] = []

        for object_name in level["is_objects"]:
            if object_name in object_to_level:
                raise ValueError(f"[schema.py] object {object_name} assigned to multiple levels: {object_to_level[object_name]} and {level_name}.")
            level_to_object[level_name].append(object_name)
            object_to_level[object_name] = level_name
        
        level_to_level[level_name] = []

        for child_level in level["child_levels"]:
            level_to_level[level_name].append(child_level)
        
        if level_to_level[level_name] == []:
            level_to_level[level_name].append(".")  # terminal level

    return level_to_object, object_to_level, level_to_level

_LEVEL_TO_OBJECT, _OBJECT_TO_LEVEL, _LEVEL_TO_LEVEL \
    = _parse_schema(_SCHEMA)

def object_to_level(object_: str) -> str:
    is_ = _OBJECT_TO_LEVEL.get(object_, None)
    if is_ is None:
        raise ValueError(f"[schema.py] object {object_} not found in schema.")
    return is_

def level_to_level() -> dict:
    return _LEVEL_TO_LEVEL