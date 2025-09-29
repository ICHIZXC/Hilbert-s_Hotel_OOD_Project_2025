class HashTable:
    def __init__(self, size: int = 101):
        self.count = 0         
        self.load_factor = 0.7
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def __str__(self):
        lines = []
        for i, bucket in enumerate(self.table):
            if bucket:
                lines.append(f"Bucket {i}: {bucket}")
        return "\n".join(lines)

    def hash_key(self, key) -> int:
        return hash(key) % self.size
    
    def is_prime(self,n):
        if n < 2:
            return False
        if n % 2 == 0 and n > 2:
            return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0:
                return False
        return True

    def next_prime(self,n):
        while not self.is_prime(n):
            n += 1
        return n
    
    def resize(self):
        new_size = self.next_prime(self.size * 2) 
        new_table = [[] for _ in range(new_size)]
        for bucket in self.table:
            for k, v in bucket:
                new_index = hash(k) % new_size
                new_table[new_index].append((k, v))
        self.size = new_size
        self.table = new_table

    def insert(self, key, value):
        if (self.count + 1) / self.size > self.load_factor:
            self.resize()
        bucket_index = self.hash_key(key)
        bucket = self.table[bucket_index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1 

    def search(self, key):
        bucket_index = self.hash_key(key)
        bucket = self.table[bucket_index]
        for k, v in bucket:
            if key == k:
                return v
        return None

    def remove(self, key):
        bucket_index = self.hash_key(key)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                del bucket[i]
                return True
        return False