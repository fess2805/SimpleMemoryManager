from interface import implements, Interface

class IMemoryManager(Interface):
    def init(self, size, sizeOfSpace): 
        pass
    def allocate_memory(self, process):
        pass
    def release_memory(self, process):
        pass
    def get_status(self):
        pass
    

#void Init(int size);
#void Init(int size, int sizeOfSpace);
#void AddTask(Task task, CancellationToken token);
#void ClearTask(Task task);
#void UnloadMemorySpace(Guid id);
#void LoadMemorySpace(Guid id, CancellationToken token);
#void GetStatus(StatusModel status);