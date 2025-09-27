# This is main program 
from AVL import AVL
from HashMap import HashTable
import time

<<<<<<< Updated upstream
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
        
    @timer
    def search(self, room_num):
        return self.hash.search(room_num)
    
    @timer
    def remove(self, room_num):
        if self.hash.search(room_num):
            self.avl.delete_node(room_num)
            self.hash.remove(room_num)
            
=======
>>>>>>> Stashed changes
