from parser import parse
import schema
from stack import PopulatorStack
from populator import PopulatorData


def _get_level_from_tag(tag: str) -> str:
    return schema.object_to_level(tag)


def _process_text(text: str) -> dict:
    data = PopulatorData()
    stack = PopulatorStack(
        push_schema=schema.level_to_level(),
    )
    for obj, meta in parse(text):
        tag_type, uuid, *rest = meta

        if tag_type == "tag":
            data.add(obj, uuid)
            level = _get_level_from_tag(obj["tag"])

            for q in stack.push((uuid, level)):
                q_uuid, _ = q
                p_uuid = stack.peek_uuid()
                if p_uuid == "root": break # stop at root
                data.apply_child(p_uuid, q_uuid)

        elif tag_type == "content":
            if stack.is_empty():
                raise ValueError(f"[processor.py] no parent tag available for content/newline with uuid {uuid}.")
            data.apply_content(stack.peek_uuid(), obj)

        elif tag_type == "newline":
            if stack.is_empty():
                continue  # skip newlines outside of any tagobj
            data.apply_content(stack.peek_uuid(), obj)

    # clear the stack and route remaining items
    for q in stack.clear():
        q_uuid, _ = q
        p_uuid = stack.peek_uuid()
        if p_uuid == "root": break  # stop at root
        data.apply_child(p_uuid, q_uuid)

    return data.to_dict()


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