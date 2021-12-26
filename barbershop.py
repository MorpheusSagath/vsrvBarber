import threading
import time
import random

global NUMBER_OF_SEATS
NUMBER_OF_SEATS = 2
global NUMBER_OF_CUSTOMERS
NUMBER_OF_CUSTOMERS = 5

global WORK_TIME
WORK_TIME = 3.1
global SLEEP_PRX
SLEEP_PRX = 0

global count, start
count = 0
start = 0

mutex = threading.Lock()
customerSemaphore = threading.Semaphore(0)
barberSemaphore = threading.Semaphore(0)

def tPrint(str):
    global start
    mutex.acquire()
    print("[{0:4.1f}] {1}".format((time.time()-start), str), flush=True)
    mutex.release()
    return

def newHair():
    time.sleep(0.1)
    tPrint('... Парикмахер пригласил клиента, свободных мест стало: {0}'.format(NUMBER_OF_SEATS - count))
    time.sleep(WORK_TIME)
    tPrint('... Парикмахер закончил стрижку')

def barber():
    global count
    while True:
        if count == 0:
            tPrint('*** Парикмахер решил вздремнуть ***')
            while barberSemaphore.acquire(blocking = False):    # сброс счетчика
                barberSemaphore.acquire()                       # семафора до 0
            if not barberSemaphore.acquire(timeout = 10):
                break
        else:
            mutex.acquire()
            count-=1
            mutex.release()
            newHair()
            customerSemaphore.release()
            time.sleep(0.1)

def customer():
    global count
    th_name = threading.current_thread().name
    if count < NUMBER_OF_SEATS:
        tPrint('=> Пришел {0}. Сел на кресло для ожидания, осталось свободных кресел: {1}'.format(th_name, NUMBER_OF_SEATS-(count+1)))
        mutex.acquire()
        count+=1
        mutex.release()

        barberSemaphore.release()
        customerSemaphore.acquire()

        tPrint('<= {0} постригся и уходит'.format(th_name))
    else:
        tPrint('<= {0} видит, что все места заняты и уходит'.format(th_name))


start = time.time()
tPrint('● Запуск >> всего мест:{0} всего клиентов:{1} время стрижки:{2}с ●'.format(NUMBER_OF_SEATS, NUMBER_OF_CUSTOMERS, WORK_TIME))

# запуск потока парикмахера
threadBar = threading.Thread(name='Парикмахер', target=barber)
threadBar.start()

#запуск потоков-клиентов
threadsCust = []
for i in range(0, NUMBER_OF_CUSTOMERS):
   tr = threading.Thread(name='Клиент {0}'.format(i), target=customer)
   threadsCust.append(tr)
   tr.start()
   time.sleep(random.random()+SLEEP_PRX)

# ожидание завершения потока парикмахера
threadBar.join()
tPrint('● клиентов долго нет, закрываем парикмахерскую ●')