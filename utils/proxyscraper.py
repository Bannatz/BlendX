import requests
import json

class ProxyScraper:
    def __init__(self, method):
        self.method = method
    
    def proxy_scrape(self, timeout, protocol, ssl):
        proxy_list = []
        if ssl == None:
            ssl = 'all'
        elif timeout == 0:
            timeout = 10000
        elif protocol == None:
            protocol = 'all'
        try:
            proxies = requests.get(f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country=all&ssl={ssl}&anonymity=all')
            proxies = proxies.text.split("\n")
            proxy_list.extend([proxy.strip() for proxy in proxies])
            return proxy_list
        except requests.exceptions.RequestException as e:
            return [e]
    
    def all_apis(self, anon: str, protocol: str, speed: int, limit: str):
        apis = [f"https://www.proxy-list.download/api/v1/get?type={protocol}&anon={anon}",f"https://proxylist.geonode.com/api/proxy-list?anonymityLevel={anon}&protocols={protocol}&speed={speed}&limit={limit}&page=1&sort_by=lastChecked&sort_type=desc"]
        # proxy-list.download -> Text Output
        # proxylist.geonode.com -> json output
        proxies = []
        if speed is None:
            speed = "fast"
        if anon is None:
            anon = "elite"
        if limit is None:
            limit = 500

        for api in apis:
            try:
                resp = requests.get(api)
                if 'application/json' in resp.headers['Content-Type'].lower():
                    res = resp.json()
                    for info in res['data']: # There are many more types of info you can Extract. I will write it in the README.
                        ip = info['ip']
                        port = info['port']
                        proxies.append(f"{ip}:{port}")
                else:
                    r = resp.text
                    proxies.extend(r.split("\n"))
                    pass
                print(proxies)
            except requests.exceptions.RequestException as e:
                print(f"Failed to Obtain Proxy: {e}")
        return proxies