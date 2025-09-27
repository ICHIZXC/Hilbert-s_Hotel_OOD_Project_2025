class HashTable:
    def __init__(self, size: int = 100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def __str__(self):
        for i, bucket in enumerate(self.table):
            if bucket and len(bucket) != 0:
                print(f"Bucket {i}: {bucket}")
        return ""

    def hash_key(self, key) -> int:
        return key % self.size

    def insert(self, key, value):
        bucket_index = self.hash_key(key)
        bucket = self.table[bucket_index]
        bucket.append((key, value))

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