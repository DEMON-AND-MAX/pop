class PopulatorData:
    class DataItem:
        def __init__(self, uuid: str, tag: str, ref: str):
            self.uuid = uuid
            self.tag = tag
            self.ref = ref
            self.children = []
            self.content = []
        
        def add_child(self, child_uuid: str):
            if child_uuid in self.children:
                raise ValueError(f"[populator.py] child {child_uuid} already exists in children of {self.uuid}.")
            self.children.append(child_uuid)
        
        def add_content(self, content: str):
            self.content.append(content)
        
        def to_dict(self) -> dict:
            return {
                "uuid": self.uuid,
                "tag": self.tag,
                "ref": self.ref,
                "children": self.children,
                "content": self.content,
            }

    def __init__(self):
        self.data = {}

    def add(self, object: dict, uuid: str):
        if uuid in self.data:
            raise ValueError(f"[populator.py] object with uuid {uuid} already exists.")
        
        self.data[uuid] = self.DataItem(
            uuid=uuid,
            tag=object.get("tag"),
            ref=object.get("ref"),
        )

    def _get(self, uuid: str) -> DataItem:
        is_ = self.data.get(uuid, None)
        if not is_:
            raise ValueError(f"[populator.py] object {uuid} not found in data.")
        return is_
    
    def apply_child(self, obj_uuid: str, child_uuid: str):
        obj = self._get(obj_uuid)
        obj.add_child(child_uuid)
    
    def apply_content(self, obj_uuid: str, content: str):
        obj = self._get(obj_uuid)
        obj.add_content(content)
    
    def to_dict(self) -> dict:
        result = {}
        for uuid, item in self.data.items():
            result[uuid] = item.to_dict()
        return result

    