class SharedMemoryV1:
    def __init__(self):
        self.memo = {}

    def get(self, key, default=None):
        return self.memo.get(key, default)

    def add(self, key, value):
        self.memo[key] = value

    def update(self, key, value):
        self.memo[key] = value

    def remove(self, key):
        if key in self.memo:
            del self.memo[key]

    def add_conversation(self, prompt, response):
        if 'conversations' not in self.memo:
            self.memo['conversations'] = []
        self.memo['conversations'].append({"prompt": prompt, "response": response})

    def get_conversations(self):
        return self.memo.get('conversations', [])