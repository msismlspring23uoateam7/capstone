import pandas as pd

class SharedMemory:

    memo = {}

    def __init__(self):
        self.memo = {}

    def get(self, key):
        return self.memo[key]

    def add(self, key, value):
        self.memo[key] = value

    def update(self, key, value):
        self.memo[key] = value

    def remove(self, key):
        del self.memo[key]

    def keys(self):
        return self.memo.keys()