from IMemory import IMemoryManager
from Space import Space
from process import Process
from interface import implements, Interface
import threading
import random

class VariablePartitionMemoryManager(implements (IMemoryManager)):
    def __init__(self, size, sizeOfSpace, compress):
        self.Mutex = threading.Lock()
        self.Spaces = list()
        self.totalSize = size
        self.countPages = 0
        self.fillPages = 0
        self.filSizes = 0
        self.compress = compress
        cells = [2,4,6,8]   
        countSize = 0     
        while countSize < size:            
            for i in range(4):
                sizeOfSpace = cells[i]
                if ((countSize + sizeOfSpace) <= size):
                    space = Space(sizeOfSpace)
                    self.Spaces.append(space)
                    self.countPages += 1     
                    countSize += sizeOfSpace
        self.Spaces.sort(key=lambda item: item.size)   
    
    def compress_memory(self):
        position = self.countPages - 1
        while True:
            is_compress = False
            checkSpace = self.Spaces[position]
            if (((checkSpace.size - checkSpace.busySize) < 2 and checkSpace.locked == True) or checkSpace.locked == False):
                position -= 1
                if (position < self.countPages / 2): break
                else: continue                
            for freeSpace in self.Spaces:
                if (freeSpace.locked == False and freeSpace.size >= checkSpace.busySize and freeSpace.size != checkSpace.size):
                    freeSpace.process = checkSpace.process
                    if (freeSpace.process != None): freeSpace.process.clear_space()
                    freeSpace.process.add_space(freeSpace) 
                    freeSpace.locked = True
                    checkSpace.locked = False
                    is_compress = True
                    position -= 1
                    break
            if (is_compress == False or position < self.countPages / 2):
                break

                    

    
    def allocate_memory(self, process: Process):
        self.Mutex.acquire()  
        findSpace = False           
        for space in self.Spaces:
            if (space.locked == False and space.size >= process.size):
                findSpace = True
                space.process = process
                space.locked = True
                space.busySize = process.size
                self.fillPages +=1
                self.filSizes += process.size
                process.add_space(space)                 
                break  
        if (findSpace == False and self.compress):
            self.compress_memory()
        self.Mutex.release()

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in self.Spaces:
            if (space.process == process):
                space.locked = False                
                self.fillPages -=1
                self.filSizes -= process.size
                break
        process.clear_space()
        self.Mutex.release()

    def get_status(self):
        return f"Менеджер памяти с переменными разделами: Занято разделов: {self.fillPages} Занято памяти: {self.filSizes}"
    def wakeup_process(self, process: Process):
        return


