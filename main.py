# This is main program 
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

    def calculate_room_number(self, guest: int, car: int, plane: int, fleet: int) -> int:
        return (2**person) * (3**car) * (5** ship) * (7**fleet)
    
    @timer
    def add_room(self, person: int, car: int, ship: int, fleet: int):
        room_number = self.calculate_room_number(person, car, ship, fleet)
        
        room_data = (person, car, ship, fleet)
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
    def 
            

hotel = Hotel(size=100)

initial_guest = int(input("Initail Guest: "))
for i in range(initial_guest) :
    hotel.add_room(0, 0, 0, i)
print(hotel.hash)
while (True) :
    print("===================================")
    print("MENU: ")
    print("1. add guest")
    print("2. print sort room")
    print("3. print empty room")
    print("4. search room")
    print("5. remove room")
    print("6. save to file")
    print("x. exit..")
    opt = input("select: ")
    if opt == '1' :
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("1.  add n guest")
        print("2.  add n guest on m bus")
        print("3.  add n guest on m bus on l ship")
        print("4.  add n guest on m bus on l ship in k fleet")
        opt = input("select: ")
        if opt == "1" :
            print("add n guest")
            n = int(input("n = "))
            for a in range(n) : hotel.add_room(0, 0, 0, a)
        elif opt == "2" :
            print("add n guest on m bus")
            n = int(input("n = "))
            m = int(input("m = "))
            for b in range(m) :
                for a in range(n) : hotel.add_room(0, 0, b, a)
        elif opt == "3" :
            print("add n guest on m bus on l ship")
            n = int(input("n = "))
            m = int(input("m = "))
            l = int(input("l = "))
            for c in range(l) :
                for b in range(m) :
                    for a in range(n) : hotel.add_room(0, c, b, a)
        elif opt == "4" :
            print("add n guest on m bus on l ship in k fleet")
            n = int(input("n = "))
            m = int(input("m = "))
            l = int(input("l = "))
            k = int(input("k = "))
            for d in range(k) :
                for c in range(l) :
                    for b in range(m) :
                        for a in range(n) : hotel.add_room(d, c, b, a)

    elif opt == '2' :
        print("Sorted Rooms:", hotel.sort_rooms())
    elif opt == '3' :
        print("Empty Rooms:", hotel.empty_rooms())
    elif opt == '4' :
        room_number = int(input("room number : "))
        print("Find room",room_number,":", hotel.find_room(room_number))
    elif opt == '5' :
        room_number = int(input("room number : "))
        hotel.remove_room(room_number)
    elif opt == '6' :
        hotel.save_to_file("./hotel_rooms.csv")
    elif opt == 'x' :
        break
    else :
        print("selection invalid!")
