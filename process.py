import uuid
from Space import Space

class Process():
    def __init__(self, size):
        self.id = uuid.uuid4()
        self.size = size        
        self.status = 0
        self.countSpaces = 0
        self.Spaces = []
    
    def add_space(self, space):
        self.Spaces.append(space)
        self.countSpaces += 1