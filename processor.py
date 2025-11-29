from parser import parse
import schema
from stack import PopulatorStack


def _apply_child(data: dict, obj_uuid: str, child_uuid: str):
    """
    for the data dictionary, apply `child_uuid` to the `children` field of object `obj_uuid`
    """
    if obj_uuid == "root":
        return
    
    obj = data.get(obj_uuid)

    if not obj:
        raise ValueError(f"[processor.py] object {obj_uuid} not found in data.")
    if "children" not in obj:
        raise ValueError(f"[processor.py] object {obj_uuid} has no `children` field.")
    
    obj["children"].append(child_uuid)


def _get_level_from_tag(tag: str) -> str:
    return schema.object_to_level(tag)


def _process_text(text: str) -> dict:
    data = {}
    stack = PopulatorStack(
        push_schema=schema.level_to_level(),
    )
    for obj, meta in parse(text):
        tag_type, uuid, *rest = meta
        if tag_type == "tag":
            data[uuid] = obj
            level = _get_level_from_tag(obj["tag"])
            for q in stack.push((uuid, level)):
                q_uuid, _ = q
                _apply_child(data, stack.peek_uuid(), q_uuid)
        elif tag_type == "content":
            if stack.is_empty():
                raise ValueError(f"[processor.py] no parent tag available for content/newline with uuid {uuid}.")
            _apply_child(data, stack.peek_uuid(), obj)
        elif tag_type == "newline":
            if stack.is_empty():
                continue  # skip newlines outside of any tagobj
            _apply_child(data, stack.peek_uuid(), obj)

    # clear the stack and route remaining items
    for q in stack.clear():
        q_uuid, _ = q
        _apply_child(data, stack.peek_uuid(), q_uuid)

    return data


if __name__ == "__main__":
    """
    test the text processor with a sample text
    """
    sample_text = """
    // this is a comment
    [page ref-001]
    
    [section ref-002]
    // another comment

    12345 Some content here.
    67890 More content.

    [text ref-003]

    texty stuff here.

    [text ref-004]
    even more texty stuff.
    """

    data = _process_text(sample_text)

    import json
    print(json.dumps(data, indent=4))