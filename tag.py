from copy import deepcopy

SCHEMA = {
    "tag": "",
    "uuid": "",
    "ref": "",
    "children": []
}

ARGS_INDEX = {
    "tag": 0,
    "uuid": 1,
    "ref": 2,
}

def _apply_args(args: list[str], schema:dict, args_index: dict) -> dict:
    # sanity checks
    if not args or len(args) == 0:
        raise ValueError("[tag_processor.py] no `args` provided.")
    if not schema or len(schema) == 0:
        raise ValueError("[tag_processor.py] no `schema` provided.")
    if not args_index or len(args_index) == 0:
        raise ValueError("[tag_processor.py] no `args_index` provided.")
    if len(args) != len(ARGS_INDEX):
        raise ValueError("[tag_processor.py] `args` does not match `args_index`.")

    # apply each argument to the schema
    for key, index in args_index.items():
        schema[key] = args[index]
    
    return schema

def process_tag(tag: str, args: list[str]):
    # object based on the schema
    obj = _apply_args([tag, *args], deepcopy(SCHEMA), ARGS_INDEX)

    return obj


if __name__ == "__main__":
    """
    1. test normal use-case
    2. check too many args
    3. check too few args
    """
    import json

    # 1. test normal use-case
    obj = process_tag("div", ["1234-5678", "ref-001"])

    print("1. test normal use-case")
    print(json.dumps(obj, indent=4))

    # 2. check too many args
    try:
        obj = process_tag("div", ["1234-5678", "ref-001", "extra-arg"])
    except ValueError as e:
        print("\n2. check too many args")
        print(e)
    
    # 3. check too few args
    try:
        obj = process_tag("div", ["1234-5678"])
    except ValueError as e:
        print("\n3. check too few args")
        print(e)