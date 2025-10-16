from Treap import Treap
import pandas as pd
from HashMap import HashTable
import time
from pprint import pprint
from pympler import asizeof
import itertools


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
        self.treap = Treap()
        self.hash = HashTable(size)
        self.max_room_num = 0
        self.dimensions = []
        self.primes_cache = []
        self.guest_status_marker = "old"

    def is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def generate_primes(self, n):
        # Only generate new primes if we need more
        if len(self.primes_cache) >= n:
            return self.primes_cache[:n]
        
        # Start from where we left off
        if self.primes_cache:
            num = self.primes_cache[-1] + 1
        else:
            num = 2
        
        # Generate only the additional primes needed
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
        
        # Check if room exists (single search)
        if self.hash.search(room_num) is not None:
            # Collision resolution - find next available room
            i = 1
            room_num += i ** 2
            while self.hash.search(room_num) is not None:
                i += 1
                room_num += i ** 2
        
        # Create details dictionary in one go
        details = {self.dimensions[i]: values[i] for i in range(len(values))}
        details['status'] = self.guest_status_marker
        if is_initial:
            details['initial'] = True
        
        # Insert into both data structures
        self.hash.insert(room_num, details)
        self.treap.add(room_num)
        self.max_room_num = max(self.max_room_num, room_num)

        return room_num


    @timer
    def search(self, room_num):
        return self.hash.search(room_num)
    
    @timer
    def delete(self, room_num):
        if self.hash.search(room_num):
            self.treap.delete_node(room_num)
            self.hash.remove(room_num)

    @timer
    def write_file(self, file_name: str):
        if not file_name:
            print("Error: File name cannot be empty")
            return False
        
        try:
            # Use list comprehension for better performance
            data = [(key, value.get('status', 'old')) 
                    for bucket in self.hash.table if bucket
                    for key, value in bucket if value]
            
            # Sort in-place
            data.sort(key=lambda x: x[0])
            
            df = pd.DataFrame(data, columns=["Room Number", "Guest Status"])
            df.to_csv(file_name, index=False)
            print(f"Successfully saved to {file_name}")
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False    

    @timer
    def sort(self):
        return self.treap.inorder()
    
    @timer
    def memory_usage(self):
        return asizeof.asizeof(self.hash) + asizeof.asizeof(self.treap)

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
    
    def add_manual_room(self, room_num: int):
        
        if room_num < 0:
            print("Error: Room number cannot be negative")
            return False
        
        self.mark_all_guests_as_old()
        self.guest_status_marker = "new"
            
        if self.hash.search(room_num) is not None:
            ans = input(f"Room number {room_num} is already occupied, do you want to replace?\n(1) Yes\n(2) No\nSelect Command : ")
            if ans == '1':
                start = time.perf_counter()
                self.treap.delete_node(room_num)
                self.hash.remove(room_num)
                details = {"manually added": '', 'status': self.guest_status_marker}
                self.hash.insert(room_num, details)
                self.treap.add(room_num)
                self.max_room_num = max(self.max_room_num, room_num)
                end = time.perf_counter()
                elapsed = end - start
                print(f"Successfully replaced and added manual room {room_num}")
                print(f"\nadd_manual_room runtime: {elapsed:.6f} sec")
                return True
            elif ans == '2':
                print("Discarded")
                return False
            else:
                print("Invalid Input")
                return False
        
        start = time.perf_counter()
        details = {"manually added": '', 'status': self.guest_status_marker}
        self.hash.insert(room_num, details)
        self.treap.add(room_num)
        self.max_room_num = max(self.max_room_num, room_num)
        end = time.perf_counter()
        elapsed = end - start
        print(f"Successfully added manual room {room_num}")
        print(f"\nadd_manual_room runtime: {elapsed:.6f} sec")
        return True
    
    def mark_all_guests_as_old(self):
        for bucket in self.hash.table:
            for _, details in bucket:
                if details is not None:
                    details['status'] = 'old'

    def prepare_for_new_guests(self):
        self.mark_all_guests_as_old()
        self.guest_status_marker = "new"
        print("Hotel ready for new guest arrivals")

    def add_dimension(self, dimension_name: str):
        if not dimension_name:
            print("Error: Dimension name cannot be empty")
            return -1
        
        if dimension_name in self.dimensions:
            print(f"Error: Way '{dimension_name}' already exists")
            return -1
        
        self.dimensions.append(dimension_name)
        for bucket in self.hash.table:
            for _, details in bucket:
                if details is not None:
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

    def add_guests_nested(self):
        import itertools
        
        print("\n=== Add Guests with Nested Ways ===")
        print("Each way contains the next way\n")
        
        try:
            counts = []
            for i, way in enumerate(self.dimensions):
                if i == 0:
                    count = int(input(f"How many {way}? "))
                else:
                    count = int(input(f"How many {way} per {self.dimensions[i-1]}? "))
                
                if count < 0:
                    print(f"Error: Cannot have negative {way}")
                    return False
                counts.append(count)
            
            total = 1
            for c in counts:
                if c > 0:
                    total *= c
            
            if total == 0:
                print("Error: Total guests would be 0")
                return False
            
            print(f"\nTotal guests to add: {total}")
            print(f"Calculation: {' × '.join(map(str, counts))} = {total}")
            
            confirm = input("Confirm? (y/n): ")
            if confirm.lower() != 'y':
                print("Cancelled")
                return False
            
            self.mark_all_guests_as_old()
            self.guest_status_marker = "new"
            
            start = time.perf_counter()
            ranges = [range(1, c + 1) for c in counts]
            
            for combo in itertools.product(*ranges):
                values = list(combo)
                self.add_room(values)
            
            end = time.perf_counter()
            elapsed = end - start
            
            print(f"Successfully added {total} guests")
            print(f"\nadd_guests_nested runtime: {elapsed:.6f} sec")
            return True
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers.")
            return False

hotel = Hotel()

try:
    n_dimensions = int(input("Enter number of initial arrival ways: "))
    if n_dimensions < 1:
        print("Invalid Input: Must have at least 1 arrival way")
        exit()
except ValueError:
    print("Error: Invalid input. Please enter a valid number.")
    exit()

for i in range(n_dimensions):
    dim_name = input(f"Enter name for arrival way {i+1}: ").strip()
    if not dim_name:
        print("Error: Arrival way name cannot be empty")
        exit()
    hotel.dimensions.append(dim_name)

print("\nCurrent arrival ways:", hotel.dimensions)
print("You can add new parallel ways of arrival using option (10)")

try:
    initial_guest = int(input("Initial Guest: "))
    if initial_guest < 0:
        print("Invalid Input: Cannot have negative guests")
        exit()
except ValueError:
    print("Error: Invalid input. Please enter a valid number.")
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
    print("(13) Add Guests with Nested Ways")
    print("(x) Exit")
    
    print("----------𝘗𝘭𝘦𝘢𝘴𝘦 𝘴𝘦𝘭𝘦𝘤𝘵 𝘺𝘰𝘶𝘳 𝘤𝘰𝘮𝘮𝘢𝘯𝘥----------")
    cmd = input("Select Command : ")
    if cmd == '1':
        if len(hotel.dimensions) == 0:
            print("Error: No arrival ways defined. Please add at least one way first.")
            continue
        
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
            result = hotel.search(room_num)
            if result is not None:
                print(f"Search Room {room_num} : {result}")
            else:
                print(f"Room {room_num} not found")
        except ValueError:
            print("Error: Invalid room number")
    elif cmd == '3':
        try:
            room_num = int(input("Enter Room Number : "))
            if hotel.hash.search(room_num) is not None:
                hotel.delete(room_num)
                print(f"Successfully deleted room {room_num}")
            else:
                print(f"Error: Room {room_num} does not exist")
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
        new_dim = input("Enter new way name: ").strip()
        if not new_dim:
            print("Error: Way name cannot be empty")
        else:
            dim_index = hotel.add_dimension(new_dim)
            if dim_index >= 0:
                print(f"Added new way '{new_dim}' at index {dim_index}")
                print(f"Current ways: {hotel.dimensions}")
    elif cmd == '10':
        if len(hotel.dimensions) == 0:
            print("Error: No arrival ways defined.")
            continue
        
        try:
            print("Available way(s):", hotel.dimensions)
            dim_name = input("Enter way's name: ").strip()
            if not dim_name:
                print("Error: Way name cannot be empty")
            elif dim_name in hotel.dimensions:
                value = int(input(f"Enter {dim_name} value to track: "))
                results = hotel.track_by_dimension(dim_name, value)
                print(f"Found {len(results)} rooms with {dim_name}={value}:")
                for room_num, details in results:
                    print(f"Room {room_num}: {details}")
            else:
                print("Error: Way not found!")
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
        dim_name = input("Enter way name to remove: ").strip()
        if not dim_name:
            print("Error: Way name cannot be empty")
        else:
            hotel.remove_dimension(dim_name)
    elif cmd == '13':
        if len(hotel.dimensions) == 0:
            print("Error: No arrival ways defined. Please add at least one way first.")
            continue
        
        hotel.add_guests_nested()
    elif cmd == 'x':
        break
    else:
        print("Invalid Selection")