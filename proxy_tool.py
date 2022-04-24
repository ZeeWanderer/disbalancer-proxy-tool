#!/usr/bin/env python3

import json
import requests
from jsonpath import JSONPath

protocols_set: set[str] = {"socks5", "socks4", "https", "http"}
proxies_set: set[str] = set()

class ProxyData(object):
    def __init__(self, data):
        # define variables for autocomplete
        self.url: str = ""
        self.protocol: str = ""
        self.format: str = ""
        self.path: str = "" # Optional
        
        self.__dict__ = data 

def proxy_sort(el: str):
    protocol = el.split("://")[0]
    return protocol_priority[protocol]

# load configuration
config: dict
with open("./config.json", "r") as config_f:
    config = json.load(config_f)
proxy_links: dict[str, list[str]] = config["proxies"]
protocol_priority = config["protocol_priority"]

# load proxies
for object_ in proxy_links:
    proxy_data = ProxyData(object_)

    try:
        print(f"Downloading proxies from {proxy_data.url}...")
        proxyfile_r = requests.get(proxy_data.url)
    except requests.exceptions.RequestException as e:
        print(f"Unable to download proxies from {proxy_data.url}, error: {e}.")
        continue
    
    # handle plaintext format
    if proxy_data.format == "plaintext":
        try:
            if proxy_data.protocol not in protocols_set:
                print(f"Unknown protocol {proxy_data.format} for plaintext format, skipping processing.")
                continue

            proxyfile = proxyfile_r.text
            proxylines = [f"{proxy_data.protocol}://{line}" for line in proxyfile.replace("\r\n", "\n").split("\n") if line]
            proxies_set.update(proxylines)
            print(f"Downloaded {len(proxylines)} {proxy_data.protocol} proxies.")
        except Exception as e:
            print(f"Unable to process proxies from {proxy_data.url}, error: {e}.")
            continue
    # handle json format
    elif proxy_data.format == "json":
        try:
            json_objects = proxyfile_r.json()

            ip_path, port_path = proxy_data.path.split("|")
            ip_list = JSONPath(ip_path).parse(json_objects)
            port_list = JSONPath(port_path).parse(json_objects)

            if proxy_data.protocol in protocols_set:
                protocol_list = [proxy_data.protocol] * len(ip_list)
            else:
                protocol_list = JSONPath(proxy_data.protocol).parse(json_objects)

                # handle APIs that provide protocol type only once per request
                if len(protocol_list) != len(ip_list) and len(protocol_list) == 1:
                    protocol_list = protocol_list * len(ip_list)

            proxylines = [f"{protocol}://{ip}:{port}" for protocol, ip, port in zip(protocol_list, ip_list, port_list)]
            proxies_set.update(proxylines)
            print(f"Downloaded {len(proxylines)} proxies.")
        except Exception as e:
            print(f"Unable to process proxies from {proxy_data.url}, error: {e}.")
            continue
    # handle unknown formats
    else:
        print(f"Unknown format {proxy_data.format}, skipping processing.")
        continue

# tally and dump proxies to file
if len(proxies_set) != 0:
    print(f"Finished downloading proxies.\nUnique proxies:")
    proxies_list: list[str] = list(proxies_set)
    for protocol in protocols_set:
        res = sum(map(lambda i: i.startswith(protocol), proxies_list))
        print(f"\t{protocol.upper()}: {res}")

    print(f"\tTOTAL: {len(proxies_set)}")

    print(f"Dumping to proxies.txt...")
    with open("./proxies.txt", "w") as proxies_f:
        proxies_list_str = "\n".join(sorted(proxies_list, key=proxy_sort))
        proxies_f.write(proxies_list_str)
    print(f"Success.")
else:
    print(f"No proxies to dump.")