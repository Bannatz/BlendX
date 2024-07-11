# BlendX
BlendX is a versatile tool designed for crafting, managing user and email combos and includes scraping and checking Proxies. The Frontend is powered by DearPyGui.
# BIG DISCLAIMER
**I do not condone any form of Criminal Activities with this Tool.**

## Why this Project ?
BlendX aims to combine multiple functionalities into a single tool, addressing the need for efficient management of user and email combinations alongside proxy scraping and checking capabilities.

## How to use it ?
Install all dependencies: `$ pip install -r requirements.txt`.
Then just run the `main.py` file.

## Features
### ProxyScraper:
- Proxyscrape: BlendX includes support for Proxyscrape. It is in my Opinion one of the best Free Proxy Sites ive found. I could be wrong though!

- All APIs Method: Scrape all **FREE** APIs that i could find! Feel free to add Your API to the list of apis in `proxyscraper.py`.
It should check if the respond is a json format or not. If your API sends data through json feel free to modify the Function.

#### Side Note
Paid APIs can be added but my focus is only in **free** APIs. I personally cant test Paid Services.

### ProxyChecker:
- Multithreaded Proxy Checker that checks if Proxy can connect to Google. Timeout, SSL Support and Protocol Type can be choosen if `Proxyscrape` method is used. I try to add it to `All APIs` Method.

### Combo Editor:

- Delete Dupes: Easily remove duplicate entries from combo lists to maintain clean and efficient data.

- Organize Combos: Sort and organize combo lists to streamline - data management.

- Remove @ Prefix: Specifically remove the @ prefix from email entries for specialized use cases + Mail2User: Strip mail domains from a combo to gather a username

### How to use the Google Dork Generator:
<span style="color:red;">**ATTENTION**</span>

**It should be said that Google Ratelimits because of that i need to make that request with a Proxy.
That said Proxy can be scraped with this Program. But if you like you can add your own.
<span style="color:yellow;">With Free Proxies that Request can take a little longer.</span>**

The site keyword is for filtering which URL should be displayed. Example: `site:pastebin.com` results in only pastebin urls.

The inurl keyword searches for specific text in the URL. Example `inurl:login`.

The intitle Textbox is for the Titles. Example: `intitle: Pastebin`. The Search Results are only URLs that have Pastebin in title.

The filetype Textbox is for the File Type in the URLs. Example: `filetype: .pdf` Results are only `.pdf` files.

There are many more but i cant add them all to a Textbox. There would be too much in the Frontside because of that i add a `Advanced Dork Gen` Window to the Frontend. That contains all "Advanced" Queries like `range:`, `stocks:`, `loc`, `allintitle:` and so on.

If you click `Generate Dorks` i want to try to combine all common filetypes that are used.
you can add multiple "keywords" to the inurl keyword. It results in generating multiple dorks based on those keywords.

### Theme Editor:

- Theme Creation: Customize and create themes according to personal preferences.

- Edit Fonts: Manage and modify fonts to achieve desired visual aesthetics and readability in the interface.

### Utils:
The Utils Folder can be used in any Python Project.

The `textutils.py` file provides functionalities for text file manipulation.

**Example Usage of this Class:**
```python
import textutils

file_path = "example.txt"
lines_to_save = ["line 1", "line 2", "line 3"]

# Save lines to file
success = Text_Edit.save_txt(file_path, lines_to_save)
if success:
    print("File saved successfully!")
else:
    print("Failed to save file.")

# Load lines from file
loaded_lines = Text_Edit.load_txt(file_path)
print("Loaded lines:", loaded_lines)

# Remove duplicates
input_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = Text_Edit.del_dupes(input_list)
print("Unique list:", unique_list)

# Sort items
unsorted_list = ["b", "a", "c"]
sorted_list = Text_Edit.sort_items(unsorted_list)
print("Sorted list:", sorted_list
```

The `proxyscraper.py` file provides Scraping Functionalities. For ProxyScrape or Free APIs.

**Example Usage of this Class:**
```python
import proxyscraper

scraper = ProxyScraper(method="All")

# Scrape proxies using all APIs
all_proxies = scraper.scrape_proxies(timeout=5000, protocol='http', ssl=None)
print("All Proxies:", all_proxies)

# Alternatively, scrape proxies using only ProxyScrape method
proxy_scrape_only = ProxyScraper(method="ProxyScrape")
proxies = proxy_scrape_only.scrape_proxies(timeout=3000, protocol='socks4', ssl='yes')
print("ProxyScrape Proxies:", proxies)
```

The `proxychecker.py` file provides methods for checking Proxies.

**Example Usage of this Class:**
```python
import proxychecker
proxy_checker = ProxyChecker()

# Example proxies list
proxies_list = [
    "192.168.1.1:8080",
    "123.45.67.89:3128",
    "socks5proxy.example.com:1080",
    "socks4proxy.example.com:1080"
]

# Example protocol and timeout
protocol = "http"
timeout = 10  # Timeout in seconds
# Perform proxy checking
print(f"\nPerforming proxy check with protocol '{protocol}' and timeout '{timeout}' seconds...")
working_proxies, failed_proxies, errored_proxies = proxy_checker.check_proxy(protocol, timeout, proxies_list)
# Print results
print("\nProxy Check Results:")
print(f"Working Proxies: {working_proxies}")
print(f"Failed Proxies: {failed_proxies}")
print(f"Errored Proxies: {errored_proxies}")
```
