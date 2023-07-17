Multithreaded Port Scanner

This is a Python script that performs a multithreaded scan for open TCP and UDP ports on a specified target IP address. It supports scanning for specific protocols, services, and vulnerabilities.


Features

Multithreaded scanning for faster port discovery
Supports TCP and UDP scanning
Scans for specific services known to use certain ports
Scans for known vulnerabilities associated with open ports
Configurable logging to a file and/or console output


Requirements

Python 3.x


Execution 

```
usage: portScanner.py [-h] [--ports PORTS [PORTS ...]] [--threads THREADS]
                      [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [--protocol {tcp,udp,both}] [--services SERVICES [SERVICES ...]]
                      [--output-file OUTPUT_FILE] [--log-to-console]
                      target

Multithreaded TCP and UDP port scanner

positional arguments:
  target                Target IP address to scan

optional arguments:
  -h, --help            show this help message and exit
  --ports PORTS [PORTS ...], -p PORTS [PORTS ...]
                        Port range to scan (default: 1-1023)
  --threads THREADS, -t THREADS
                        Number of threads for TCP and UDP scanning (default: 10)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level (default: INFO)
  --protocol {tcp,udp,both}
                        Protocol to scan: tcp, udp, or both (default: both)
  --services SERVICES [SERVICES ...]
                        Scan for specific services (e.g., http, https, ftp)
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Save the results to a file (default: scan_results.txt)
  --log-to-console      Log results to the console in addition to the output file
```
