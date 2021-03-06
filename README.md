# proxy tool
A simple tool to download proxies from various sources into a file. Made for use with [disbalancer](https://disbalancer.com/).

## Installation
 - Dearchive or clone into disbalancer folder
 - Install [Pyhon3](https://www.python.org/downloads/) if not installed
 - Install dependencies: `pip install -r ./requirements.txt`

## Usage
Run `python -O ./proxy_tool.py`, proxies will be downloaded into `proxies.txt`.  
Wait till download finishes, then start disbalancer.  
For amd64 windows there is `run-disbalancer.ps1` script.

## Config
`config.json` is a file used to store proxy list links and other configuration data.

### proxies
A proxy object list:
 - `url` - link to the proxy data. Required.
 - `format` - format of the data. Can be [`json`, `plaintext`]. For `plaintext` data the expected format is `ip:port` with new lines as delimiter. For `json`, data format is defined using `JSONPATH` expression. Required.
 - `protocol` - can be [`socks5`, `socks4`, `https`, `http`] or in case of `json` format also a `JSONPATH` expression. Required.
 - `path` - `ip_expr|protocol_expr`, where `ip_expr` and `protocol_expr` are `JSONPATH` expressions. Required for `json` format.

All mentioned `JSONPATH` expression are required to describe how to get all instances of required property as a list. For examples see [config.json](/config.json). [Jsonpath.com](https://jsonpath.com/) can be used to verify your expressions work.
