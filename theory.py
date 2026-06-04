# Сборщик мусора: напишите фрагмент кода, создающий циклическую ссылку (cyclic reference).
# С помощью модуля gc и sys.getrefcount продемонстрируйте, как увеличивается счетчик ссылок и в какой момент объект удаляется только сборщиком мусора,
# а не стандартным механизмом подсчета ссылок.
import gc
import sys
import multiprocessing
import threading
import time


class Node:
    def __init__(self, name):
        self.name = name
        self.linc = None

    def __del__(self):
        print(f'Удаление объекта {self.name}')

def demo_cyclic_reference():
    print('Создание объектов')
    a = Node('Sergay')
    b = Node('Andrey')
    a.linc = b
    b.linc = a
    print(sys.getrefcount(a) - 1)
    del b
    del a

    for obj in gc.get_objects():
        if isinstance(obj, Node):
            print(obj)

    gc.collect()

    for obj in gc.get_objects():
        if isinstance(obj, Node):
            print(obj)

def fib_1(count, fib_one = 0, fib_two = 1):
    if count == 1:
        return fib_one
    return fib_1(count - 1, fib_two, fib_one + fib_two)

def cpu_bound_task_fib(count):
    if count <= 0:
        return 0
    if count == 1:
        return 1
    return cpu_bound_task_fib(count - 1) + cpu_bound_task_fib(count - 2)

def run_threads():
    t1 = threading.Thread(target=cpu_bound_task_fib, args=(36,))
    t2 = threading.Thread(target=cpu_bound_task_fib, args=(36,))
    start = time.perf_counter()
    t1.start()
    t2.start()
    print(t1.join(), t2.join())
    print(f'Время выполнения на потоках: {time.perf_counter() - start}')

def run_processes():
    t1 = multiprocessing.Process(target=cpu_bound_task_fib, args=(36,))
    t2 = multiprocessing.Process(target=cpu_bound_task_fib, args=(36,))
    start = time.perf_counter()
    t1.start()
    t2.start()
    print(t1.join(), t2.join())
    print(f'Время выполнения на процессах: {time.perf_counter() - start}')


if __name__ == '__main__':
    demo_cyclic_reference()
    cpu_bound_task_fib(36)
    run_threads()
    run_processes()