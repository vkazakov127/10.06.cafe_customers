# -*- coding: utf-8 -*-
# 10.06.cafe_customers.py
import queue
from threading import Thread, Event
from time import sleep


class Table():  # Столик в кафе

    def __init__(self, number, is_busy):
        self.number = number
        self.is_busy = is_busy


class Cafe:  # Кафе

    def __init__(self, tables_list):
        self.tables = tables_list  # Список столиков в Кафе
        self.customers_queue = queue.Queue()

    def customer_arrival(self):  # Приход посетителя
        for customer_num in range(customer_count_max):
            print(f'Посетитель {customer_num + 1} прибыл в кафе.')
            # Передаём в обслуживание
            self.customers_queue.put(customer_num)  # В очередь
            # Следующий!
            sleep(arrival_time_interval)  # Нужно маленько передохнуть...

    def serve_customer(self, stop_event):  # Обслуживание посетителя
        while not stop_event.is_set():
            # while self.customers_queue.qsize() > 0:
            # Проверяем, есть ли свободный столик
            for table_one in self.tables:
                if not table_one.is_busy:
                    # print(f'Есть свободный столик {table_one.number + 1}')
                    try:
                        my_customer_num = self.customers_queue.get(timeout=1)  # Достаём посетителя из очереди
                    except queue.Empty:
                        stop_event.set()
                        break
                    print(f'Очередь после Посетителя №{my_customer_num + 1}: {self.customers_queue.qsize()} чел.')
                    Customer(my_customer_num)
                    table_one.is_busy = True  # Столик ЗАНЯТ
                    print(f'Посетитель {my_customer_num + 1} сел за столик {table_one.number + 1}.')
                    sleep(serv_time_duration)  # Идёт обслуживание посетителя
                    print(f'Посетитель {my_customer_num + 1} уже откушал. Приходите ещё!')
                    table_one.is_busy = False  # Столик опять свободен


class Customer:

    def __init__(self, customer_number):
        self.customer_number = customer_number


# Общие параметры приложения (заданы в условии Задачи)
arrival_time_interval = 1  # Интервал прихода посетителей, в секундах
customer_count_max = 20    # Макс. количество посетителей
serv_time_duration = 5     # Длительность обслуживания
tbl_count = 3              # Количество столиков в Кафе
# -------------------------------------------------------
# Создаём список столиков
cafe_tables = []  # Список столиков в Кафе
for i in range(tbl_count):
    cafe_tables.append(Table(i, False))

# Инициализируем кафе
cafe1 = Cafe(cafe_tables)  # Кафе со списком столиков

# Объявляем потоки
# stop_event_customer_arrival = Event() # — это оказалось не нужно
stop_event_serve_customer = Event()     # — а вот это нужно
# Поток для прибытия посетителей (швейцар)
customer_arrival_thread = Thread(target=cafe1.customer_arrival)
# Поток для обслуживания посетителей (официант)
serve_customer_thread = Thread(target=cafe1.serve_customer, args=(stop_event_serve_customer, ))

# start
customer_arrival_thread.start()
serve_customer_thread.start()

# join
customer_arrival_thread.join()
serve_customer_thread.join()

print('------ The End ------')
