from IMemory import IMemoryManager
from VariablePartitionMemoryManager import VariablePartitionMemoryManager
import threading
import random
import time
from process import Process

memoryManager = VariablePartitionMemoryManager(64, 8)
count_worked_process = 0
count_working_process = 0

def access_resource(timer, process):    
    global memoryManager, count_worked_process, count_working_process   
    # выполняем обработку
    time.sleep(timer)    
    #print(f'{process.id} закончил выполнение. Выгружаем память...') 
    memoryManager.release_memory(process)
    #print(f'{process.id} освободил память.')
    count_worked_process += 1  
    count_working_process -= 1

def main_thread(all_task):
    global memoryManager, count_working_process    
    for i in range(all_task):
        process = Process(random.randint(1,8))
        #print(f'{process.id} пробует получить память для загрузки')    
        while True:
            memoryManager.allocate_memory(process)
            if process.countSpaces == 0:
                time.sleep(0.1)
                continue
            process.status = 1
            break
        #print(f'{process.id} получил память для загрузки. Начинаем выполнение...') 
        count_working_process +=1
        thread = threading.Thread(target=access_resource, daemon=True, args=(random.randint(5,10), process, ))
        thread.start()


#создадим процессы
all_task = 100
thread = threading.Thread(target=main_thread, daemon=True, args=(all_task, ))
thread.start()
count_second = 0
while count_worked_process != all_task:
    time.sleep(1)
    count_second += 1
    print(memoryManager.get_status())
    print(f"Кол. работающих: {count_working_process}, Задач: {count_worked_process}/{all_task}, Секунд: {count_second}")
    








