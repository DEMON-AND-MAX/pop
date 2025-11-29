from parser import parse

def _apply_child(data: dict, obj_uuid: str, child_uuid: str):
    """
    for the data dictionary, apply `child_uuid` to the `children` field of object `obj_uuid`
    """
    obj = data.get(obj_uuid)

    if not obj:
        raise ValueError(f"[processor.py] object {obj_uuid} not found in data.")
    if "children" not in obj:
        raise ValueError(f"[processor.py] object {obj_uuid} has no `children` field.")
    
    obj["children"].append(child_uuid)


def _process_text(text: str) -> dict:
    data = {}
    stack = []
    for obj, meta in parse(text):
        tag_type, uuid, *rest = meta
        if tag_type == "tag":
            data[uuid] = obj
            stack.append(uuid)
        elif tag_type == "content":
            if not stack:
                raise ValueError(f"[processor.py] no parent tag available for content/newline with uuid {uuid}.")
            data[uuid] = obj
            _apply_child(data, stack[-1], uuid)
        elif tag_type == "newline":
            if not stack:
                continue  # skip newlines outside of any tag
            data[uuid] = obj
            _apply_child(data, stack[-1], uuid)
    
    return data


if __name__ == "__main__":
    """
    test the text processor with a sample text
    """
    sample_text = """
    // this is a comment
    [div ref-001]
    
    [span ref-002]
    // another comment

    12345 Some content here.
    67890 More content.

    [p ref-003]


    """

    data = _process_text(sample_text)

    import json
    print(json.dumps(data, indent=4))