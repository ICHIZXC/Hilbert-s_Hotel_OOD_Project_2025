from AVL import AVL
import pandas as pd
from HashMap import HashTable
import time
from pprint import pprint
from pympler import asizeof


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        elapsed = end - start
        print(f"\n{func.__name__} runtime: {elapsed:.6f} sec")
        return result
    return wrapper


class Hotel:
    def __init__(self, size = 101):
        self.avl = AVL()
        self.hash = HashTable(size)
        self.root = None
        self.max_room_num = 0
        self.dimensions = []
        self.primes_cache = []
        self.guest_status_marker = "old"

    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def generate_primes(self, n):
        if not self.primes_cache or len(self.primes_cache) < n:
            self.primes_cache = []
            num = 2
            while len(self.primes_cache) < n:
                if self.is_prime(num):
                    self.primes_cache.append(num)
                num += 1
        return self.primes_cache[:n]

    def calculate_room_number(self, values: list) -> int:
        primes = self.generate_primes(len(values))
        room_num = 1
        for i, value in enumerate(values):
            room_num *= ((value + 1) ** primes[i])
        return room_num
    
    def add_room(self, values: list, is_initial=False):
        room_num = self.calculate_room_number(values)
        details = {self.dimensions[i]: values[i] for i in range(len(values))}
        details['status'] = self.guest_status_marker
        if is_initial:
            details['initial'] = True

        current_room = self.hash.search(room_num)
        if current_room is None:
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
                    details_list = []
                    if value:
                        if 'initial' in value and value['initial']:
                            details_list.append('initial')
                        elif 'manually added' in value:
                            details_list.append('manual')
                        else:
                            for dim in self.dimensions:
                                if dim in value and value[dim] != 0:
                                    details_list.append(dim)
                        details_list.append(value.get('status', 'old'))
                    details_tuple = tuple(details_list)
                    data.append((key, details_tuple))
        
        data.sort(key=lambda x: x[0])
        
        df = pd.DataFrame(data, columns=["Room Number", "Details"])
        df.to_csv(file_name, index=False)    

    @timer
    def sort(self):
        return self.avl.inorder()
    
    @timer
    def memory_usage(self):
        return asizeof.asizeof(self.hash) + asizeof.asizeof(self.root)

    @timer
    def guest_count(self) -> int:
        occupied_rooms = sum(1 for bucket in self.hash.table for _, value in bucket if value is not None)
        return occupied_rooms
    
    def guest_status_summary(self):
        old_count = 0
        new_count = 0
        for bucket in self.hash.table:
            for _, details in bucket:
                if details is not None:
                    status = details.get('status', 'old')
                    if status == 'old':
                        old_count += 1
                    else:
                        new_count += 1
        return old_count, new_count
    
    @timer  
    def add_manual_room(self, room_num: int):
        
        if room_num < 0:
            print("Error: Room number cannot be negative")
            return False
        
        self.mark_all_guests_as_old()
        self.guest_status_marker = "new"
            
        if self.hash.search(room_num) is not None:
            ans = input(f"Room number {room_num} is already occupied, do you want to replace?\n(1) Yes\n(2) No\nSelect Command : ")
            if ans == '1':
                self.avl.delete_node(room_num)
                self.hash.remove(room_num)
                details = {"manually added": '', 'status': self.guest_status_marker}
                self.hash.insert(room_num, details)
                self.avl.add(room_num)
                self.max_room_num = max(self.max_room_num, room_num)
                print(f"Successfully replaced and added manual room {room_num}")
                return True
            elif ans == '2':
                print("Discarded")
                return False
            else:
                print("Invalid Input")
                return False
        
        details = {"manually added": '', 'status': self.guest_status_marker}
        self.hash.insert(room_num, details)
        self.avl.add(room_num)
        self.max_room_num = max(self.max_room_num, room_num)
        print(f"Successfully added manual room {room_num}")
        return True
    
    def mark_all_guests_as_old(self):
        for bucket in self.hash.table:
            for _, details in bucket:
                if details is not None:
                    if 'initial' not in details and 'manually added' not in details:
                        details['status'] = 'old'

    def prepare_for_new_guests(self):
        self.mark_all_guests_as_old()
        self.guest_status_marker = "new"
        print("Hotel ready for new guest arrivals")

    def add_dimension(self, dimension_name: str):
        self.dimensions.append(dimension_name)
        for bucket in self.hash.table:
            for _, details in bucket:
                if details is not None:
                    # Only add dimension to non-initial, non-manual rooms
                    if 'initial' not in details and 'manually added' not in details:
                        details[dimension_name] = 0
        return len(self.dimensions) - 1

    def remove_dimension(self, dimension_name: str):
        if dimension_name not in self.dimensions:
            print(f"Error: Way '{dimension_name}' does not exist")
            return False
        
        if len(self.dimensions) <= 1:
            print("Error: Cannot remove the last arrival way. At least one way must remain.")
            return False
        
        self.dimensions.remove(dimension_name)
        
        for bucket in self.hash.table:
            for _, details in bucket:
                if details and dimension_name in details:
                    del details[dimension_name]
        
        print(f"Successfully removed way '{dimension_name}'")
        print(f"Remaining ways: {self.dimensions}")
        return True

    @timer
    def track_by_dimension(self, dimension_name: str, value: int) -> list:
        if dimension_name not in self.dimensions:
            return []
        
        result = []
        for bucket in self.hash.table:
            for room_num, details in bucket:
                if details is not None and dimension_name in details:
                    if details[dimension_name] == value:
                        result.append((room_num, details))
        return result

hotel = Hotel()

n_dimensions = int(input("Enter number of initial arrival ways: "))
if n_dimensions < 1:
    print("Invalid Input")
    exit()
print("Enter names for each way guests can arrive (e.g. from_cars, from_buses, from_planes)")
for i in range(n_dimensions):
    dim_name = input(f"Enter name for arrival way {i+1}: ")
    hotel.dimensions.append(dim_name)

print("\nCurrent arrival ways:", hotel.dimensions)
print("You can add new parallel ways of arrival using option (10)")

initial_guest = int(input("Initial Guest: "))
if initial_guest < 0:
    print("Invalid Input")
    exit()
start = time.perf_counter()
for i in range(initial_guest):
    values = [i] + [0] * (len(hotel.dimensions) - 1)
    hotel.add_room(values, is_initial=True)
end = time.perf_counter()
print("\nTotal runtime:", end - start)

while(True):
    print(" ----------𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝕳𝖎𝖑𝖙𝖘𝖇𝖊𝖗𝖙-𝕻𝖔𝖗𝖙𝖆𝖑----------")
    print("Catalog : ")
    print("(1) Add Guest")
    print("(2) Search Room")
    print("(3) Delete Room")    
    print("(4) Print Hashed Room")
    print("(5) Print Sorted Room")
    print("(6) Save File")
    print("(7) Memory Used")
    print("(8) Guest Count")
    print("(9) Add New Way")
    print("(10) Track by Way")
    print("(11) Add Manual Room")
    print("(12) Remove Arrival Way")
    print("(x) Exit")
    
    print("----------𝘗𝘭𝘦𝘢𝘴𝘦 𝘴𝘦𝘭𝘦𝘤𝘵 𝘺𝘰𝘶𝘳 𝘤𝘰𝘮𝘮𝘢𝘯𝘥----------")
    cmd = input("Select Command : ")
    if cmd == '1':
        try:
            values = []
            valid_input = True
            for i, dim in enumerate(hotel.dimensions):
                count = int(input(f"Enter number of {dim}(s): "))
                if count < 0:
                    print("Error: Cannot add negative guests")
                    valid_input = False
                    break
                values.append(count)
            
            if not valid_input:
                continue
            
            hotel.mark_all_guests_as_old()
            hotel.guest_status_marker = "new"
            
            start = time.perf_counter()
            for dim_idx in range(len(values)):
                for guest_num in range(1, values[dim_idx] + 1):
                    current_values = [0] * len(values)
                    current_values[dim_idx] = guest_num
                    hotel.add_room(current_values)
            
            end = time.perf_counter()
            print("\nTotal runtime:", end - start)
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    elif cmd == '2':
        try:
            room_num = int(input("Enter Room Number : "))
            print("Search Room", room_num," : ", hotel.search(room_num))
        except ValueError:
            print("Error: Invalid room number")
    elif cmd == '3':
        try:
            room_num = int(input("Enter Room Number : "))
            hotel.delete(room_num)
        except ValueError:
            print("Error: Invalid room number")
    elif cmd == '4':
        print(hotel.hash)
    elif cmd == '5':
        print("Sorted Room : ", end = '')
        hotel.sort()
    
    elif cmd == '6':
        hotel.write_file("./hotel-room_lists.csv")
    elif cmd == '7':
        print(f"Memory used : {hotel.memory_usage()} byte(s)")
    elif cmd == '8':
        print("Guest Count : ", hotel.guest_count())
    elif cmd == '9':
        new_dim = input("Enter new way name: ")
        dim_index = hotel.add_dimension(new_dim)
        print(f"Added new way '{new_dim}' at index {dim_index}")
        print(f"Current ways: {hotel.dimensions}")
    elif cmd == '10':
        try:
            print("Available way(s):", hotel.dimensions)
            dim_name = input("Enter way's name: ")
            if dim_name in hotel.dimensions:
                value = int(input(f"Enter {dim_name} value to track: "))
                results = hotel.track_by_dimension(dim_name, value)
                print(f"Found {len(results)} rooms with {dim_name}={value}:")
                for room_num, details in results:
                    print(f"Room {room_num}: {details}")
            else:
                print("Way not found!")
        except ValueError:
            print("Error: Invalid input")
    elif cmd == '11':
        try:
            room_num = int(input("Enter room number to add: "))
            hotel.add_manual_room(room_num)
        except ValueError:
            print("Error: Invalid room number")
    elif cmd == '12':
        print("Current arrival ways:", hotel.dimensions)
        dim_name = input("Enter way name to remove: ")
        hotel.remove_dimension(dim_name)
    elif cmd == 'x':
        break
    else:
        print("Invalid Selection")