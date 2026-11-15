import time
import requests
from concurrent.futures import ThreadPoolExecutor
import threading

# Defined once but thread_local object is created for every thread under the hood
thread_local = threading.local() 

def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 500
    start_time = time.perf_counter()
    download_all_sites(sites)
    total_time = time.perf_counter() - start_time
    print(f"It took {total_time} seconds")

def download_all_sites(sites):
    # Thread pool automatically creates 5 threads and handles the distribution of workload across available threads
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(download_site, sites)
    
def download_site(url):
    # Each thread gets its own session from thread_local with thread safety
    session = get_session()
    with session.get(url) as response:
        print(f'Read {len(response.content)} bytes for site {url}')

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

if __name__ == "__main__":
    main()