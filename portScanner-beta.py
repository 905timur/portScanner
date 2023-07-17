import argparse
import socket
import threading
from queue import Queue
import logging

logger = logging.getLogger(__name__)

KNOWN_SERVICES = {
    'http': 80,
    'https': 443,
    'ftp': 21,
    # Add more known services and ports as needed
}

KNOWN_VULNERABILITIES = {
    # Add known vulnerabilities and their associated ports here
}

def portscan(target, port, dtype):
    try:
        sock = socket.socket(socket.AF_INET, dtype)
        sock.connect((target, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def tcp_worker(target, queue, result_file, log_to_console=False):
    while True:
        port = queue.get()
        if portscan(target, port, socket.SOCK_STREAM):
            logger.info(f'TCP Port {port} is open!')
            result_file.write(f'TCP Port {port} is open!\n')
        else:
            logger.debug(f'TCP Port {port} is closed!')
            result_file.write(f'TCP Port {port} is closed!\n')
        
        if log_to_console:
            print(f'TCP Port {port} is open!' if portscan(target, port, socket.SOCK_STREAM)
                  else f'TCP Port {port} is closed!')
        queue.task_done()

def udp_worker(target, queue, result_file, log_to_console=False):
    while True:
        port = queue.get()
        if portscan(target, port, socket.SOCK_DGRAM):
            logger.info(f'UDP Port {port} is open!')
            result_file.write(f'UDP Port {port} is open!\n')
        else:
            logger.debug(f'UDP Port {port} is closed!')
            result_file.write(f'UDP Port {port} is closed!\n')
        
        if log_to_console:
            print(f'UDP Port {port} is open!' if portscan(target, port, socket.SOCK_DGRAM)
                  else f'UDP Port {port} is closed!')
        queue.task_done()

def main(target, port_range, num_threads, log_level, protocol, services, output_file, log_to_console):
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    file_handler = logging.FileHandler(output_file)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    queue = Queue()
    for port in port_range:
        queue.put(port)

    with open(output_file, 'w') as result_file:
        if protocol in ['tcp', 'both']:
            for _ in range(num_threads):
                t = threading.Thread(target=tcp_worker, args=(target, queue, result_file, log_to_console))
                t.daemon = True
                t.start()

        if protocol in ['udp', 'both']:
            for _ in range(num_threads):
                t = threading.Thread(target=udp_worker, args=(target, queue, result_file, log_to_console))
                t.daemon = True
                t.start()

        queue.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded TCP and UDP port scanner')
    parser.add_argument('target', help='Target IP address to scan')
    parser.add_argument('--ports', '-p', type=int, nargs='+', default=range(1, 1024),
                        help='Port range to scan (default: 1-1023)')
    parser.add_argument('--threads', '-t', type=int, default=10,
                        help='Number of threads for TCP and UDP scanning (default: 10)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help='Logging level (default: INFO)')
    parser.add_argument('--protocol', choices=['tcp', 'udp', 'both'], default='both',
                        help='Protocol to scan: tcp, udp, or both (default: both)')
    parser.add_argument('--services', nargs='+', choices=KNOWN_SERVICES.keys(),
                        help='Scan for specific services (e.g., http, https, ftp)')
    parser.add_argument('--output-file', '-o', default='scan_results.txt',
                        help='Save the results to a file (default: scan_results.txt)')
    parser.add_argument('--log-to-console', action='store_true',
                        help='Log results to the console in addition to the output file')

    args = parser.parse_args()
    main(args.target, args.ports, args.threads, args.log_level, args.protocol,
         args.services, args.output_file, args.log_to_console)
