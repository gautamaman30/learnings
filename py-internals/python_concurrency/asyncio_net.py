import time

# asyncio uses event loop and coroutines to handle concurrency on single thread, it works well until you have a blocking code
import asyncio
import aiohttp

async def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 500
    start_time = time.perf_counter()
    await download_all_sites(sites)
    total_time = time.perf_counter() - start_time
    print(f"It took {total_time} seconds")

async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = [download_site(url, session) for url in sites]
        await asyncio.gather(*tasks, return_exceptions=True)
    
async def download_site(url, session):
    async with session.get(url) as response:
        print(f'Read {len(await response.read())} bytes for site {url}')

if __name__ == "__main__":
    asyncio.run(main())