from parser import parse
from populator import Populator


def _process_text(text: str) -> dict:
    populator = Populator()

    for obj, meta in parse(text):
        populator.populate(obj, meta)

    return populator.wrangle()


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