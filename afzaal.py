import sys
import asyncio
import aiohttp

async def enumerate_subdomains(url, output_format="txt"):
    live_subdomains = []

    with open('wordlist.txt', 'r') as wordlist_file:
        wordlist = [line.strip() for line in wordlist_file]

    async with aiohttp.ClientSession() as session:
        tasks = []

        async def check_subdomain(subdomain):
            full_url = f"http://{subdomain}.{url}"
            try:
                async with session.get(full_url, timeout=5) as response:
                    if response.status == 200:
                        status = "L"
                        live_subdomains.append(f"{full_url} ({status})")
                    else:
                        status = "X"
                    if output_format == "json":
                        print(f'{{"url": "{full_url}", "status": "{status}"}}')
                    else:
                        print(f"{full_url} ({status})")
            except aiohttp.ClientError:
                pass

        for subdomain in wordlist:
            task = asyncio.ensure_future(check_subdomain(subdomain))
            tasks.append(task)

        await asyncio.gather(*tasks)

    if output_format != "json":
        print("\nLive Subdomains:")
        for subdomain in live_subdomains:
            print(subdomain)

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-u":
        print("Usage: afzaal.py -u http://example.com")
        sys.exit(1)

    url = sys.argv[2]

    print(f"Checking subdomains for {url}:\n")

    output_format = "txt"  # Change to "json" to output results in JSON format
    asyncio.run(enumerate_subdomains(url, output_format))

if _name_ == "_main_":
    main()
