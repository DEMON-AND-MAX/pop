from itertools import count

from tag import process_tag

def _sanitize_and_split(text: str) -> list[str]:
    lines = text.splitlines()
    sanitized_lines = [line.strip() for line in lines]
    return sanitized_lines

def _get_line_type(line: str) -> str:
    if line.startswith("[") and line.endswith("]"):
        return "tag"
    if line.startswith("//"):
        return "comment"
    if line == "":
        return "newline"
    
    return "content"

def _split_line(line: str) -> list[str]:
    # remove the square brackets
    tag_content = line[1:-1].strip()
    # split by whitespace
    parts = tag_content.split()
    return parts

# iterate through each line and yield processed objects
def parse(text: str):
    lines = _sanitize_and_split(text)

    # parse lines and generate uuid on the go
    for line, uuid in zip(lines, count()):
        line_type = _get_line_type(line)
        match line_type:
            case "tag":
                # always yield a dict
                tag, *args = _split_line(line)
                yield process_tag(tag, [str(uuid), *args]), line_type, tag
            case "content":
                # always yield a string
                yield line, line_type
            case "newline":
                # always yield a string `\n`
                yield "\n", line_type
            case "comment":
                # skip comment line
                continue
            case _:
                raise ValueError(f"[parser.py] unknown line type: {line}")
    
    return None

if __name__ == "__main__":
    """
    test the parser with a sample text
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

    for obj in parse(sample_text):
        print(obj)