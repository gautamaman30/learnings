import time
import requests
import atexit
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

session: requests.Session

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
    # Process pool automatically creates your python program process by default equal to number of cpu cores on the computer 
    # they handle the distribution of workload across available processes
    with ProcessPoolExecutor(initializer=init_process) as executor:
        executor.map(download_site, sites)
    
def download_site(url):
    with session.get(url) as response:
        process_name = multiprocessing.current_process().name
        print(f'{process_name}: Read {len(response.content)} bytes for site {url}')

def init_process():
    # init_process assign the session globally for each process, so that session can be reused in download_site fn
    global session
    session = requests.Session()
    # to prevent memory leaks
    atexit.register(session.close)

if __name__ == "__main__":
    main()