import os
import time

import django
from django.core.cache import cache
from django.test import Client


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def request_courses(client):
    start = time.time()
    response = client.get('/api/courses/')
    elapsed = time.time() - start
    return response, elapsed


def main():
    print("=== Testing Public Course Cache ===\n")

    cache.clear()
    client = Client()

    print("First call to /api/courses/ ...")
    response1, time1 = request_courses(client)
    print(f"Status: {response1.status_code}")
    print(f"First call time: {time1:.4f}s\n")

    print("Second call to /api/courses/ (cached) ...")
    response2, time2 = request_courses(client)
    print(f"Status: {response2.status_code}")
    print(f"Second call time: {time2:.4f}s\n")

    print("=== Summary ===")
    print(f"First call: {time1:.4f}s")
    print(f"Second call: {time2:.4f}s")
    if time2 > 0:
        print(f"Perbandingan: second call {time1 / time2:.2f}x lebih cepat")


if __name__ == '__main__':
    main()
