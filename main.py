from AVL import AVL
import pandas as pd
from HashMap import HashTable
import time

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
        self.max_room_number = 0

    def calculate_room_number(self, guest: int, car: int, plane: int, town: int, country:int, continent:int) -> int:
        return (2**guest) * (3**car) * (5**plane) * (7**town) * (11**country) * (13**continent)

    @timer
    def add_room(self, guest: int, car: int, plane: int, town: int, country:int, continent:int):
        room_number = self.calculate_room_number(guest, car, plane, town, country, continent)
        details = {
            'continent': continent,
            'country': country,
            'town': town,
            'plane': plane,
            'car': car,
            'guest': guest
        }
        
        room_data = (guest, car, plane, town, country, continent)
        self.hash.insert(room_number, room_data)

        self.avl.add(room_number)
        self.max_room_number = max(self.max_room_number, room_number)

        return room_number

    @timer
    def search(self, room_num):
        return self.hash.search(room_num)
    
    @timer
    def remove(self, room_num):
        if self.hash.search(room_num):
            self.avl.delete_node(room_num)
            self.hash.remove(room_num)

    @timer
    def write_file(self, file_name: str):
        data = []
        for bucket in self.hash.table:
            if bucket:
                for key, value in bucket:
                    data.append((key, value))
        df = pd.DataFrame(data, columns=["Room Number", "Details"])
        df.to_csv(file_name, index=False)

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

