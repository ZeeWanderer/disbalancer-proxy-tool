#!/usr/bin/env pwsh
python -OO ./proxy_tool.py
./launcher-disbalancer-go-client-windows-amd64.exe -stats 5s
