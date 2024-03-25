from IMemory import IMemoryManager
from Space import Space
from process import Process
from interface import implements, Interface
import threading
import random

class VariablePartitionMemoryManager():
    def __init__(self, size, sizeOfBlocs) -> None:
        self.Mutex = threading.Lock()
        self.Spaces = dict()
        self.totalSize = size
        self.countPages = 0
        self.fillPages = 0
        self.filSizes = 0
        cells = [2,4,6,8]   
        countSize = 0     
        while countSize < size:
            sizeOfSpace = cells[random.randint(0,3)]
            if ((countSize + sizeOfSpace) <= size):
                space = Space(sizeOfSpace)
                self.Spaces[space.id] = space
                self.countPages += 1     
                countSize += sizeOfSpace   
    
    def allocate_memory(self, process: Process):
        self.Mutex.acquire()             
        for space in self.Spaces.values():
            if (space.locked == False and space.size >= process.size):
                space.process = process
                space.locked = True
                space.busySize = process.size
                self.fillPages +=1
                self.filSizes += process.size
                process.add_space(space)                 
                break  
        self.Mutex.release()

    def release_memory(self, process):
        self.Mutex.acquire()
        for space in self.Spaces.values():
            if (space.process == process):
                space.locked = False                
                self.fillPages -=1
                self.filSizes -= process.size
                break
        self.Mutex.release()

    def get_status(self):
        return f"Менеджер памяти с постоянными разделами: Занято разделов: {self.fillPages} Занято памяти: {self.filSizes}"


