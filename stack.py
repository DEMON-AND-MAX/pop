class Stack:
    def __init__(self):
        self._stack = []

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self._stack.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self._stack[-1]
        return None

    def is_empty(self):
        return len(self._stack) == 0
    
    def size(self):
        return len(self._stack)

# boilerplate stack logic that only allows pushing
# gives error when pushing invalid levels
class PopulatorStack:
    class StackItem:
        def __init__(self, uuid: str, level: str):
            self.uuid = uuid
            self.level = level

    def __init__(self, push_schema: dict):
        self._stack = self._init_stack()
        self._push_schema = self._validate_schema(push_schema)
    
    def _init_stack(self) -> Stack:
        stack = Stack()
        stack.push(self.StackItem(uuid="root", level="lvl0"))
        return stack
    
    def _validate_schema(self, schema: dict) -> dict:
        if not schema or len(schema) == 0:
            raise ValueError("[stack.py] no schema provided.")
        # additional checks can be added here
        return schema

    def _pop(self):
        item = self._stack.pop()
        if not item:
            raise ValueError("[stack.py] cannot pop from empty stack.")
        return item

    # always returns at least root
    def _peek(self) -> StackItem:
        return self._stack.peek()
    
    def _peek_level(self) -> str:
        top_item = self._stack.peek()
        if not top_item:
            raise ValueError("[stack.py] stack is empty, cannot peek level.")
        return top_item.level

    def peek_uuid(self) -> str:
        top_item = self._stack.peek()
        if not top_item:
            raise ValueError("[stack.py] stack is empty, cannot peek uuid.")
        return top_item.uuid

    def is_empty(self) -> bool:
        return self._stack.size() <= 1  # only root remains

    def clear(self):
        while self._stack.size() > 1:  # keep root
            popped_item = self._pop()
            yield (popped_item.uuid, popped_item.level)

    def _can_push(self, level: str) -> bool:
        top_level = self._peek_level()

        # avoid recursion
        if top_level == level:
            raise ValueError(f"[stack.py] cannot push same level {level} on top of itself.")

        allowed_push_levels = self._push_schema.get(top_level, None)
        if not allowed_push_levels:
            raise ValueError(f"[stack.py] no push schema defined for level {top_level}.")
        
        return level in allowed_push_levels
    
    def _should_pop(self, level: str) -> bool:
        top_level = self._peek_level()

        # can always pop if same level
        if top_level == level:
            return True
        
        allowed_push_levels = self._push_schema.get(top_level, None)
        if not allowed_push_levels:
            raise ValueError(f"[stack.py] no push schema defined for level {top_level}.")
        
        return not level in allowed_push_levels
    
    def push(self, item: tuple[str, str]):
        item = self.StackItem(*item)

        while self._should_pop(item.level):
            popped_item = self._pop()
            yield (popped_item.uuid, popped_item.level)
        
        if not self._can_push(item.level):
            raise ValueError(f"[stack.py] cannot push level {item.level} on top of {self._peek_level()}.")

        self._stack.push(item)
        return None