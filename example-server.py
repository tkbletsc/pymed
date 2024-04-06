#!/usr/bin/python3

import socket
import argparse

def handle_service(client_socket):
    try:
        
        # Receive 4 bytes from the client
        cmd_data = client_socket.recv(4)
        print(f"Received: {cmd_data} ({cmd_data.hex(' ')})")
        
        # Send the response to the client
        print("Sending pong...")
        client_socket.sendall(b'pong')
    finally:
        # Close the connection
        client_socket.close()

def handle_client_connection(port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the specified port
    server_socket.bind(('0.0.0.0', port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    
    print(f"Server is listening on port {port}...")
    
    try:
        while True:
            # Accept incoming connection
            client_socket, addr = server_socket.accept()
            print("Connection accepted from:", addr)
            
            # Handle the connection
            handle_service(client_socket)
    except KeyboardInterrupt:
        print(f"Server on port {port} shutting down...")
    finally:
        # Close the server socket
        server_socket.close()
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pymed server: receive and process requests to turn a virtual LED on or off.")
    
    # Add arguments
    parser.add_argument("port", type=int, help="Port number to listen")

    args = parser.parse_args()
    
    handle_client_connection(args.port)
    
