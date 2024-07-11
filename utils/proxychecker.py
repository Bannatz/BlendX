import requests
import concurrent.futures
import time
import dearpygui.dearpygui as dpg 

# Define ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProxyChecker:
    def check_proxy(self, protocol, timeout: int, proxies: list):
        url = "http://www.google.com"
        working_proxies = []
        failed_proxies = []
        errored_proxies = []

        def check_single_proxy(proxy):
            proxies_dict = {}

            # Build proxies dictionary based on protocol
            if protocol == "http":
                proxies_dict = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            elif protocol == "socks4":
                proxies_dict = {
                    "http": f"socks4://{proxy}",
                    "https": f"socks4://{proxy}"
                }
            elif protocol == "socks5":
                proxies_dict = {
                    "http": f"socks5://{proxy}",
                    "https": f"socks5://{proxy}"
                }
            else:
                print(f"{Colors.WARNING}Unsupported protocol: {protocol}.{Colors.ENDC}")
                errored_proxies.append(proxy)
                return

            try:
                print(f"Checking Proxy: {proxy} with Protocol: {protocol}")
                start_time = time.time()
                resp = requests.get(url, proxies=proxies_dict, timeout=timeout)
                end_time = time.time()
                if resp.status_code == 200:
                    elapsed_time = end_time - start_time
                    print(f"{Colors.OKGREEN}Proxy: {proxy}. Working. Time Elapsed: {elapsed_time:.2f} seconds.{Colors.ENDC}")
                    working_proxies.append(proxy)
                else:
                    print(f"{Colors.WARNING}Proxy: {proxy}. Status Code: {resp.status_code}.{Colors.ENDC}")
                    failed_proxies.append(proxy)
            except requests.exceptions.RequestException as e:
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"{Colors.FAIL}Proxy {proxy} failed with error: {e}. Connection time: {elapsed_time:.2f} seconds.{Colors.ENDC}")
                errored_proxies.append(proxy)
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            future_to_proxy = {executor.submit(check_single_proxy, proxy): proxy for proxy in proxies}
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"Proxy {proxy} generated an exception: {exc}")
        
        return working_proxies, failed_proxies, errored_proxies