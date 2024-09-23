# -*- coding: utf-8 -*-
#  h.10.06.py
import queue
import threading
from threading import Thread, Event
from time import sleep


class Table:  # Столы
    def __init__(self, number: int, is_busy):
        self.number = number  # Номер стола
        self.is_busy = is_busy # Стол занят


class Cafe:  # Кафе
    def __init__(self, cafe_tables: list):
        self.queue = queue.Queue()  # создаём очередь (по условию задачи именно здесь)
        self.tables = cafe_tables  # Список столов, поступает извне в аргументе
        self.customer_count_max = 10   # Количество посетителей максимальное
        self.arrival_time_interval = 1  # Интервал прихода посетителей, в секундах
        self.serv_time_duration = 5  # Длительность обслуживания Посетителя
        self.customer_served_count = 0  # Количество обслуженных посетителей (счётчик)

    def customer_arrival(self):  # Приход посетителя
        for i in range(self.customer_count_max):
            print(f'Посетитель {i + 1} прибыл в кафе.')
            cafe.queue.put(i)  # В очередь, для связи потоков
            # Следующий!
            sleep(self.arrival_time_interval)  # Нужно маленько передохнуть...

    def serve_customer(self, thread_num:int, stop_event:Event):   # Обслуживание посетителя
        while not stop_event.is_set():
            # Проверяем наличие свободных столов
            for table_i in tables:
                if not table_i.is_busy:
                    table_i.is_busy = True  # Теперь этот столик занят
                    table_index = tables.index(table_i) # Индекс столика (int) в списке
                    # Проверим очередь прибывающих посетителей
                    try:
                        customer_int = cafe.queue.get(timeout=1)
                    except queue.Empty:
                        print(f'Очередь пуста. Поток {thread_num + 1}')
                        sleep(0.1)  # Тоже для красоты печати, чтобы не накладывались друг на друга
                        break  # Выход из цикла "for"
                    print(f'Посетитель {customer_int + 1} сел за стол {table_index + 1}, поток={thread_num + 1}')
                    # Обслуживание посетителя
                    customers[customer_int].start()  # Запускаем поток Customer
                    customers[customer_int].join()  # Завершаем поток Customer
                    table_i.is_busy = False  # Теперь этот столик свободен
                    cafe.customer_served_count += 1  # Количество обслуженных Посетителей
            # Обслуживание посетителей: не пора ли прекращать потоки?
            if cafe.customer_served_count == cafe.customer_count_max:
                stop_event.set()
                print(f'stop_event={stop_event.is_set()}, поток={thread_num + 1} \n')
                break  # Выход из цикла "while"


class Customer(Thread):  # Посетитель (поток). Запускается, если есть свободные столы (по условию задачи)
    def __init__(self, user_number: int):
        super().__init__()
        self.number = user_number

    def run(self):
        sleep(cafe.serv_time_duration)  # Обслуживание посетителя
        print(f'Посетитель {self.number + 1} откушал и ушёл')


# Объекты
# Общие параметры приложения (заданы в условии Задачи)
tbl_count = 3  # Количество столиков в Кафе — должно поступать в экземпляр Cafe извне — это по условию задачи
# -------------------------------------------------------
serv_customer_threads_count = tbl_count  # Количество потоков "serv_customer_thread" оптимальное (моё)

# Создаем столики в кафе
tables = []  # Список столиков
for i in range(tbl_count):
    table = Table(i, False)
    tables.append(table)

# Инициализируем кафе
cafe = Cafe(tables)

# Объявляем потоки
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)  # Поток прибытия посетителя

# Потоки (список) для обслуживания посетителя
stop_event_serve_customer = Event()  # Для остановки потоков обслуживания
serv_customer_threads = []
for i in range(serv_customer_threads_count):  # Потоки обслуживания посетителей
    serv_customer_thread = threading.Thread(target=cafe.serve_customer, args=(i, stop_event_serve_customer))
    serv_customer_threads.append(serv_customer_thread)

# Потоки "Customer" — заданы по условию задачи, хотя они тут явно лишние
customers = []  # Список объектов (потоков) класса Customer
# Тут мы их только объявляем. Запускаются они в процедуре "cafe.serve_customer" — по условию задачи
for i in range(cafe.customer_count_max):
    customer = Customer(i)
    customers.append(customer)  # Добавляем в массив

# Запуск потоков
customer_arrival_thread.start()  # Поток прибытия посетителя
for i in range(serv_customer_threads_count):  # Потоки обслуживания посетителей
    serv_customer_threads[i].start()
    sleep(1)  # Для красивой печати, чтобы не накладывались друг на друга

# Ожидаем завершение потоков
customer_arrival_thread.join()
for i in range(serv_customer_threads_count):  # Потоки обслуживания посетителей
    serv_customer_threads[i].join()
print('---------- The End ----------')
