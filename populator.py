import schema

from stack import PopulatorStack
from data import PopulatorData

def _get_level_from_tag(tag: str) -> str:
    return schema.object_to_level(tag)

class Populator:
    def __init__(self):
        self._stack = PopulatorStack(
            push_schema=schema.level_to_level()
        )
        self._data = PopulatorData()
    
    def populate(self, object_: dict, meta: tuple):
        tag_type, uuid, *rest = meta

        if tag_type == "tag":
            self._data.add(object_, uuid)
            level = _get_level_from_tag(object_["tag"])

            for q in self._stack.push((uuid, level)):
                q_uuid, _ = q
                p_uuid = self._stack.peek_uuid()
                if p_uuid == "root": break # stop at root
                self._data.apply_child(p_uuid, q_uuid)

        elif tag_type == "content":
            if self._stack.is_empty():
                raise ValueError(f"[processor.py] no parent tag available for content/newline with uuid {uuid}.")
            self._data.apply_content(self._stack.peek_uuid(), object_)

        elif tag_type == "newline":
            if self._stack.is_empty():
                return  # skip newlines outside of any tag object
            self._data.apply_content(self._stack.peek_uuid(), object_)
    
    def wrangle(self):
        # clear the stack and route remaining items
        for q in self._stack.clear():
            q_uuid, _ = q
            p_uuid = self._stack.peek_uuid()
            if p_uuid == "root": break  # stop at root
            self._data.apply_child(p_uuid, q_uuid)
        
        return self._data.to_dict()