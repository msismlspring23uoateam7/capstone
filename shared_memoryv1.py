import pandas as pd
class SharedMemoryV1:
    def __init__(self):
        self.memo = {}
        self.conversation_counter = 0  # To track individual conversations

    # Retrieve data from memory
    def get(self, key, default=None):
        return self.memo.get(key, default)

    # Add new data to memory
    def add(self, key, value):
        self.memo[key] = value

    # Update existing data in memory
    def update(self, key, value):
        self.memo[key] = value

    # Remove data from memory
    def remove(self, key):
        if key in self.memo:
            del self.memo[key]

    # Add a conversation with additional metadata (like ID, timestamp)
    def add_conversation(self, prompt, response, conversation_id=None):
        if 'conversations' not in self.memo:
            self.memo['conversations'] = []
        
        if conversation_id is None:
            conversation_id = self.conversation_counter
            self.conversation_counter += 1

        # Store conversation metadata like ID and timestamp
        self.memo['conversations'].append({
            "id": conversation_id,
            "prompt": prompt,
            "response": response,
            "timestamp": pd.Timestamp.now()  # You can use any method to track time
        })

    # Retrieve all conversations
    def get_conversations(self):
        return self.memo.get('conversations', [])

    # Retrieve a specific conversation by ID
    def get_conversation_by_id(self, conversation_id):
        conversations = self.memo.get('conversations', [])
        for conversation in conversations:
            if conversation['id'] == conversation_id:
                return conversation
        return None

    # Retrieve the last N conversations
    def get_last_n_conversations(self, n):
        return self.memo.get('conversations', [])[-n:]

    # Clear conversation history (optional)
    def clear_conversations(self):
        self.memo['conversations'] = []