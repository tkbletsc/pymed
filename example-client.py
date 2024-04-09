#!/usr/bin/python3

import socket
import argparse

def make_request(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((hostname, port))

        # send ping
        print("Sending ping...")
        s.sendall(b'ping')
            
        # Receive and print 4 bytes
        resp_data = s.recv(4)
        print(f"Response received: {resp_data} ({resp_data.hex(' ')})")
        
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Example client: send 'ping', expect 'pong'.")

    # Add arguments
    parser.add_argument("hostname", type=str, help="Hostname or IP address")
    parser.add_argument("port", type=int, help="Port number")

    # Parse arguments
    args = parser.parse_args()

    # Call make_request function with provided arguments
    make_request(args.hostname, args.port)
    
