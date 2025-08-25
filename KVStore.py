import asyncio

_TOMBSTONE = object() 

class KVStore():
    def __init__(self):
        # store for values
        self.store = {}
        self.lock = asyncio.Lock()
        #stack keeps track of transactions and versions for rollbacks
        self.transaction_stacks = {}
    
    def _get_task_id(self):
        task = asyncio.current_task()
        if task is None:
            raise RuntimeError("No current asyncio task")
        return str(id(task))

    def _stack(self):
        tid = self._get_task_id()
        return self.transaction_stacks.setdefault(tid, [])

    def _in_tx(self):
        return bool(self._stack())

    async def set(self, key, value):
        stack = self._stack()
        if stack:
            stack[-1][key] = value
        else:
            async with self.lock:
                self.store[key] = value

    async def get(self, key):
        stack = self._stack()
        if stack:
            for tra in reversed(stack):
                if key in tra:
                    val = tra[key]
                    return None if val is _TOMBSTONE else val
        async with self.lock:
            return self.store.get(key)

    async def delete(self, key):
        stack = self._stack()
        if stack:
            stack[-1][key] = _TOMBSTONE
        else:
            async with self.lock:
                self.store.pop(key, None)

    async def begin(self):
        stack = self._stack()
        stack.append({})
    
    async def rollback(self):
        stack = self._stack()
        if not stack:
            raise RuntimeError("No transaction to rollback")
        stack.pop()
        if not stack:
            self.transaction_stacks.pop(self._get_task_id(), None)

    async def commit(self):
        stack = self._stack()
        if not stack:
            raise RuntimeError("No transaction to commit")
        previous = stack.pop()
        if stack:
            parent = stack[-1]
            parent.update(previous)
        else:
            async with self.lock:
                for key, value in previous.items():
                    if value is _TOMBSTONE:
                        self.store.pop(key, None)
                    else:
                        self.store[key] = value
                self.transaction_stacks.pop(self._get_task_id(), None)

            

        