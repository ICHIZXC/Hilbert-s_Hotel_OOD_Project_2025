from AVL import AVL
import pandas as pd
from HashMap import HashTable
import time
import sys
from pprint import pprint


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"\n{func.__name__} runtime: {end - start:.6f} sec")
        return result
    return wrapper

class Hotel:
    def __init__(self, size = 10):
        self.avl = AVL()
        self.hash = HashTable(size)
        self.root = None
        self.max_room_num = 0

    def calculate_room_number(self, guest: int, car: int, plane: int, town: int, country:int, continent:int) -> int:
        return (2**guest) * (3**car) * (5**plane) * (7**town) * (11**country) * (13**continent)

    @timer
<<<<<<< Updated upstream
    def add_room(self, guest: int, car: int, plane: int, town: int, country: int, continent: int):
        room_num = self.calculate_room_number(guest, car, plane, town, country, continent)
        details = {
            'continent': continent,
            'country': country,
            'town': town,
            'plane': plane,
            'car': car,
            'guest': guest
        }
=======
    def add_room(self, person: int, car: int, ship: int, fleet: int):
        room_number = self.calculate_room_number()
        
        room_data = (person, car, ship, fleet)
        self.hash.insert(room_number, room_data)
>>>>>>> Stashed changes

        if self.hash.search(room_num) is None:
            self.hash.insert(room_num, details)
            self.avl.add(room_num)
            self.max_room_num = max(self.max_room_num, room_num)
        else:
            i = 1
            while self.hash.search(room_num) is not None:
                room_num += i ** 2
                i += 1
            self.hash.insert(room_num, details)
            self.avl.add(room_num)
            self.max_room_num = max(self.max_room_num, room_num)

        return room_num


    @timer
    def search(self, room_num):
        return self.hash.search(room_num)
    
    @timer
    def delete(self, room_num):
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
        return self.avl.inorder()
    
    @timer
    def blank_room(self) -> int:
        total_room = self.max_room_num
        taken_room = sum(len(bucket) for bucket in self.hash.table)
        return total_room - taken_room
    
    def memory_usage(self):
        return sys.getsizeof(self.hash) + sys.getsizeof(self.root)
    
    @timer
    def search_by_continent(self, continent_id:int) -> list:
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details['continent'] == continent_id:
                    result.append((room_num,details))
        return result
    
    @timer
    def search_by_country(self, country_id:int) -> list:
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details['country'] == country_id:
                    result.append((room_num,details))
        return result
    
    @timer
    def search_by_town(self, town_id:int) -> list:
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details['town'] == town_id:
                    result.append((room_num,details))
        return result
    
    @timer
    def search_by_plane(self, plane_id:int) -> list:
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details['plane'] == plane_id:
                    result.append((room_num,details))
        return result
    
    @timer
    def search_by_car(self, car_id:int) -> list:
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details['car'] == car_id:
                    result.append((room_num,details))
        return result

<<<<<<< Updated upstream
hotel = Hotel(size=10)

initial_guest = int(input("Initial Guest: "))
for i in range(initial_guest):
    hotel.add_room(i,0,0,0,0,0)
print(hotel.hash)
while(True):
    print(" ----------𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝕳𝖎𝖑𝖘𝖇𝖊𝖗𝖙-𝕳𝖔𝖙𝖊𝖑----------")
    print("Catalog : ")
    print("(1) Add Guest")
    print("(2) Search Room")
    print("(3) Delete Room")    
    print("(4) Print Sorted Room")
    print("(5) Print Blank Room")
    print("(6) Save File")

    print("(7) Find Guest from Specific Car")
    print("(8) Find Guest from Specific Plane")
    print("(9) Find Guest from Specific Town")
    print("(10) Find Guest from Specific Country")
    print("(11) Find Guest from Specific Continent")

    print("(x) Exit")
    
    print("----------𝘗𝘭𝘦𝘢𝘴𝘦 𝘴𝘦𝘭𝘦𝘤𝘵 𝘺𝘰𝘶𝘳 𝘤𝘰𝘮𝘮𝘢𝘯𝘥----------")
    cmd = input("Select Command : ")
    if cmd == '1':
        print("(1) Add U Guest") #U V W X Y Z
        print("(2) Add U Guest on V Car")
        print("(3) Add U Guest on V Car from W Plane")
        print("(4) Add U Guest on V Car from W Plane from X Town")
        print("(5) Add U Guest on V Car from W Plane from X Town in Y Country")
        print("(6) Add U Guest on V Car from W Plane from X Town in Y Country in Z Continent")
        opt = input("Select Option : ")
        if opt == '1':
            print("Add U Guest")
            u = int(input("U = "))
            for a in range(u) : 
                hotel.add_room(a,0,0,0,0,0)
        elif opt == '2':
            print("Add U Guest on V Car")
            u = int(input("U = "))
            v = int(input("V = "))
            for b in range(v):
                for a in range(u): 
                    hotel.add_room(a,b,0,0,0,0)
        elif opt == '3':
            print("Add U Guest on V Car from W Plane")
            u = int(input("U = "))
            v = int(input("V = "))
            w = int(input("W = "))
            for c in range(w):
                for b in range(v):
                    for a in range(u): 
                        hotel.add_room(a,b,c,0,0,0)
        elif opt == '4':
            print("Add U Guest on V Car from W Plane from X Town")
            u = int(input("U = "))
            v = int(input("V = "))
            w = int(input("W = "))
            x = int(input("X = "))
            for d in range(x):
                for c in range(w):
                    for b in range(v):
                        for a in range(u): 
                            hotel.add_room(a,b,c,d,0,0)
        elif opt == '5':
            print("Add U Guest on V Car from W Plane from X Town in Y Country")
            u = int(input("U = "))
            v = int(input("V = "))
            w = int(input("W = "))
            x = int(input("X = "))
            y = int(input("Y = "))
            for e in range(y):
                for d in range(x):
                    for c in range(w):
                        for b in range(v):
                            for a in range(u): 
                                hotel.add_room(a,b,c,d,e,0)
        elif opt == '6':
            print("Add U Guest on V Car from W Plane from X Town in Y Country in Z Continent")
            u = int(input("U = "))
            v = int(input("V = "))
            w = int(input("W = "))
            x = int(input("X = "))
            y = int(input("Y = "))
            z = int(input("Z = "))
            for f in range(1, z+1):  # continent 1..Z
                for e in range(1, y+1):
                    for d in range(1, x+1):
                        for c in range(1, w+1):
                            for b in range(1, v+1):
                                for a in range(1, u+1): 
                                    hotel.add_room(a,b,c,d,e,f)
    elif cmd == '2':
        room_num = int(input("Enter Room Number : "))
        print("Search Room", room_num," : ", hotel.search(room_num))
    elif cmd == '3':
        room_num = int(input("Enter Room Number : "))
        hotel.delete(room_num)
    elif cmd == '4':
        print("Sorted Room : ", end = '')
        hotel.sort()
    elif cmd == '5':
        print("Blank Room : ", hotel.blank_room())
    elif cmd == '6':
        hotel.write_file("./hotel-room_lists.csv")
    elif cmd == '7':
        car_num = int(input("Enter Car Number : "))
        print("Guest from Car Number",car_num," : ", hotel.search_by_car(car_num))
    elif cmd == '8':
        plane_num = int(input("Enter Plane Number : "))
        print("Guest from Plane Number",plane_num," : ", hotel.search_by_plane(plane_num))
    elif cmd == '9':
        town_num = int(input("Enter Town Number : "))
        print("Guest from Town Number",town_num," : ", hotel.search_by_town(town_num))
    elif cmd == '10':
        country_num = int(input("Enter Country Number : "))
        print("Guest from Country Number",country_num," : ", hotel.search_by_country(country_num))
    elif cmd == '11':
        continent_num = int(input("Enter Continent Number : "))
        print("Guest from Continent Number",continent_num," : ", hotel.search_by_continent(continent_num))
    elif cmd == 'x':
        break
    else:
        print("Invalid Selection")
=======

>>>>>>> Stashed changes
