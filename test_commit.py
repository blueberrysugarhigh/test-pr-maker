from collections import OrderedDict
import unittest
import logging

logging.basicConfig(level=logging.INFO)


class LRUCache:
    def __init__(self, capacity: int):
        logging.info("init cache")
        self.capacity = capacity
        self.cache = OrderedDict()
        logging.info("finished init cache\n--------")

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class TestLRUCache(unittest.TestCase):

    def test_get_missing_key_returns_minus_one(self):
        cache = LRUCache(2)
        self.assertEqual(cache.get(1), -1)

    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)

    def test_evicts_least_recently_used(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(3, 30)  # evicts key 1
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)
        self.assertEqual(cache.get(3), 30)

    def test_get_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.get(1)       # key 1 is now most recently used
        cache.put(3, 30)   # evicts key 2, not key 1
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), -1)
        self.assertEqual(cache.get(3), 30)

    def test_put_updates_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(1, 99)
        self.assertEqual(cache.get(1), 99)

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 10)
        cache.put(2, 20)  # evicts key 1
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)


if __name__ == "__main__":
    unittest.main()
