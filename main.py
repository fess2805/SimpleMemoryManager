from IMemory import IMemoryManager
from VariablePartitionMemoryManager import VariablePartitionMemoryManager
from ConstantPartitionMemoryManager import ConstantPartitionMemoryManager
import threading
import random
import time
from process import Process

#memoryManagerVar = VariablePartitionMemoryManager(64, False)
#memoryManagerVarWithCompress = VariablePartitionMemoryManager(64, True)
memoryManager = IMemoryManager
count_worked_process = 0
count_working_process = 0
isTheEnd = False

def access_resource(timer, process):    
    #global memoryManager, count_worked_process, count_working_process   
    global memoryManager, count_worked_process, count_working_process   
    count_working_process +=1
    # выполняем обработку
    time.sleep(timer)    
    #print(f'{process.id} закончил выполнение. Выгружаем память...') 
    memoryManager.release_memory(process)
    #print(f'{process.id} освободил память.')
    count_worked_process += 1  
    count_working_process -= 1

def main_thread(all_task):
    global memoryManager, count_working_process, count_worked_process, isTheEnd, count_second
    processes = list()     
    for i in range(all_task):
        process = Process(random.randint(1,8))
        processes.append(process)
        #print(f'{process.id} пробует получить память для загрузки')   
    #проверка менеджера памяти с постоянными разделами
    memoryManager = ConstantPartitionMemoryManager(64,8, False)
    count_working_process = 0
    count_worked_process = 0 
    count_second = 0
    for process in processes:
        while True:
            memoryManager.allocate_memory(process)
            if process.countSpaces == 0:
                time.sleep(0.1)
                continue
            process.status = 1
            break
        #print(f'{process.id} получил память для загрузки. Начинаем выполнение...') 
        thread = threading.Thread(target=access_resource, daemon=True, args=(random.randint(5,10), process, ))
        thread.start()   
    while count_working_process != 0:
        time.sleep(1)
    time.sleep(5)
    #проверка менеджера памяти с переменными разделами
    memoryManager = VariablePartitionMemoryManager(64,-1, False)
    count_working_process = 0
    count_worked_process = 0 
    count_second = 0
    for process in processes:
        while True:
            memoryManager.allocate_memory(process)
            if process.countSpaces == 0:
                time.sleep(0.1)
                continue
            process.status = 1
            break
        #print(f'{process.id} получил память для загрузки. Начинаем выполнение...')         
        thread = threading.Thread(target=access_resource, daemon=True, args=(random.randint(5,10), process, ))
        thread.start()   
    while count_working_process != 0:
        time.sleep(1)
    time.sleep(5)
    #проверка менеджера памяти с переменными разделами c сжатием
    memoryManager = VariablePartitionMemoryManager(64,-1, True)
    count_working_process = 0
    count_worked_process = 0 
    count_second = 0
    for process in processes:
        while True:
            memoryManager.allocate_memory(process)
            if process.countSpaces == 0:
                time.sleep(0.1)
                continue
            process.status = 1
            break
        #print(f'{process.id} получил память для загрузки. Начинаем выполнение...')         
        thread = threading.Thread(target=access_resource, daemon=True, args=(random.randint(5,10), process, ))
        thread.start()   
    while count_working_process != 0:
        time.sleep(1)
    isTheEnd = True



#создадим процессы
all_task = 50
thread = threading.Thread(target=main_thread, daemon=True, args=(all_task, ))
thread.start()
count_second = 0
while isTheEnd == False:
    time.sleep(1)
    count_second += 1
    print(memoryManager.get_status())
    print(f"Кол. работающих: {count_working_process}, Задач: {count_worked_process}/{all_task}, Секунд: {count_second}")
    








