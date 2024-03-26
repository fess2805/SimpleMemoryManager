from IMemory import IMemoryManager
from Space import Space
from process import Process
from interface import implements, Interface
import threading
import time

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
    
    def get_free_memory_space(self):
        for space in self.SpacesMemory.values():
                if (space.locked == False):  
                    space.busySize = 1
                    self.fillPagesMemory +=1 
                    return space
        #ищем свободную страницу для выгрузки
        for space in self.SpacesMemory.values():
            if (space.locked == True and space.process.status == 2):
                #выгружаем страницу на диск и загружаем свободную в память
                for diskSpace in self.SpacesDisk.values():
                    if (diskSpace.locked == False):
                        diskSpace.position = 0
                        space.position = 1
                        del self.SpacesMemory[space.id]
                        del self.SpacesDisk[diskSpace.id]
                        self.SpacesMemory[diskSpace.id] = diskSpace
                        self.SpacesDisk[space.id] = space
                        space.busySize = 1                              
                        self.fillPagesDisk +=1                         
                        return diskSpace
        return None            
                
        
    
    def allocate_memory(self, process: Process):
        while process.countSpaces < process.size:      
            isFind = False      
            self.Mutex.acquire()
            space = self.get_free_memory_space()
            if (space != None):
                space.locked = True
                space.process = process
                process.add_space(space) 
                isFind = True
            self.Mutex.release()            
            if isFind == False: time.sleep(0.1)
        

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in process.Spaces:
            space.locked = False
            space.process = None  
            if (space.position == 0):                          
                self.fillPagesMemory -=1
            else:                         
                self.fillPagesDisk-=1
        process.clear_space()
        self.Mutex.release()        

    def get_status(self):
        return f"Страничный менеджер памяти: Занято страниц в памяти: {self.fillPagesMemory} Занято страниц на диске: {self.fillPagesDisk}"
    
    def wakeup_process(self, process: Process):        

        for space in process.Spaces:
            if (space.position == 1): 
                while True:
                    self.Mutex.acquire()
                    isFind = False                
                    newSpace = self.get_free_memory_space()
                    if (newSpace != None):                        
                        newSpace.locked = False
                        self.fillPagesDisk -= 1                        
                        del self.SpacesMemory[newSpace.id]
                        del self.SpacesDisk[space.id]
                        self.SpacesMemory[space.id] = space
                        self.SpacesDisk[newSpace.id] = newSpace  
                        space.position = 0  
                        newSpace.position = 1                
                        isFind = True
                    self.Mutex.release() 
                    if isFind == False: time.sleep(0.1)
                    else: break
            

