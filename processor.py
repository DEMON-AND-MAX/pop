from parser import parse


def _process_text(text: str) -> dict:
    data = {}
    stack = []
    for obj, meta in parse(text):
        tag_type, uuid, *rest = meta
        data[uuid] = obj
        # placeholder stack logic
        if tag_type == "tag":
            stack.pop() if stack else None
            stack.append(uuid)
        elif tag_type in ["newline", "content"] and stack:
            data[stack[-1]]["children"].append(uuid)
    
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