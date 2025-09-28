# This is main program 
from AVL import AVL
from HashMap import HashTable
import time
import sys
import pandas as pd

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} runtime: {end - start:.6f} sec")
        return result
    return wrapper

class Hotel:
    def __init__(self, size = 10):
        self.avl = AVL()
        self.hash = HashTable(size)
        self.root = None
        self.maxRoom_num = 0
    def calRoom_num(self, continent:int, country:int, town:int, plane:int, car:int, guest:int) -> int:
        return ((continent+1)**9)*((country+1)**7)*((town+1)**5)*((plane+1)**3)*((car+1)**2)*((guest+1)**1)
    
    @timer
    def add(self, continent:int, country:int, town:int, plane:int, car:int, guest:int) -> int:
        room_num = self.calRoom_num(continent, country, town, plane, car, guest)
        details = {
            'continent': continent,
            'country': country,
            'town': town,
            'plane': plane,
            'car': car,
            'guest': guest
        }
        pass

    @timer
    def remove(self, room_num):
        if self.hash.search(room_num):
            self.avl.delete_node(room_num)
            self.hash.remove(room_num)

    @timer
    def search(self, room_num):
        return self.hash.search(room_num)     

    @timer
    def sort(self):
        result = []
        self.avl.inorder(self.root, result)
        return result
    
    @timer
    def blank_room(self) -> int:
        total_room = self.maxRoom_num
        taken_room = sum(len(bucket) for bucket in self.hash.table)
        return total_room - taken_room
    
    def memory_usage(self):
        return sys.getsizeof(self.hash) + sys.getsizeof(self.root)

hotel = Hotel(size=10)

