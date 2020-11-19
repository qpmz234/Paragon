import copy

class Sync:
    def __init__(self, synced):
        self.synced = copy.deepcopy(synced)
    def __enter__(self):
        return self.synced
    def __exit__(self, type, value, traceback):
        delattr(self, "synced")
