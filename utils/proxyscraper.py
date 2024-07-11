import requests

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
    
    def all_apis(self, timeout, protocol, ssl):
        apis = [f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country=all&ssl={ssl}&anonymity=all', "https://gimmeproxy.com/api/getProxy", "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"]
        proxies = []
        for api in apis:
            resp = request.get(api)
            if resp.headers['Content-Type'] == 'application/json':
                r = resp.json()
                proxies.expand([r["protocol"], f"{r["ip"]}:{r["port"]}"])

    def method(self):
        match self.method:
            case "All":
                self.all_apis()
            case "ProxyScrape":
                self.proxy_scrape()