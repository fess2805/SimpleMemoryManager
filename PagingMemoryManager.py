from IMemory import IMemoryManager
from Space import Space
from process import Process
from interface import implements, Interface
import threading

class PagingMemoryManager(implements (IMemoryManager)):
    def __init__(self, size, sizeOfSpace, compress):
        self.Mutex = threading.Lock()
        self.SpacesMemory = dict()
        self.SpacesDisk = dict()
        self.totalSize = size
        self.countPages = size
        self.fillPagesMemory = 0
        self.fillPagesDisk = 0
        self.filSizesMemory = 0
        self.filSizesDisk = 0
        for i in range(self.countPages):
            space = Space(1)
            self.SpacesMemory[space.id] = space
            space = Space(1)  
            self.SpacesDisk[space.id] = space
        
    
    def allocate_memory(self, process: Process):
        while process.countSpaces < process.size:            
            self.Mutex.acquire()
            for space in self.SpacesMemory.values():
                if (space.locked == False):
                    space.process = process
                    space.locked = True
                    space.busySize = process.size
                    self.fillPages +=1
                    self.filSizes += process.size
                    process.add_space(space)                 
                    break 
            #ищем  
            self.Mutex.release()
        

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in self.Spaces.values():
            if (space.process == process):
                space.locked = False                
                self.fillPages -=1
                self.filSizes -= process.size
                break
        process.clear_space()
        self.Mutex.release()        

    def get_status(self):
        return f"Менеджер памяти с постоянными разделами: Занято разделов: {self.fillPages} Занято памяти: {self.filSizes}"
    
    def wakeup_process(self, process: Process):
        return