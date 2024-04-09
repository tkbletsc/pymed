#!/usr/bin/python3

import socket
import struct
import argparse
import random

from pymed_protocol import Command,Response,aes_encrypt,aes_decrypt

GLOBAL_KEY = b'0123456789abcdef'  # 16-byte key (128 bits)

# each normal receive is not guaranteed to get the full amount, particularly if it comes in multiple packets
# this will loop and ensure we get the full intended buffer size
def receive_exact_bytes(sock, num_bytes):
    received_data = b''  # Initialize an empty byte string to store received data
    while len(received_data) < num_bytes:
        remaining_bytes = num_bytes - len(received_data)
        data = sock.recv(remaining_bytes)  # Receive data from the socket
        if not data:
            raise RuntimeError("Socket connection closed unexpectedly")
        received_data += data  # Append received data to the buffer
    return received_data

def handle_service(client_socket, mode):
    try:
        if mode=='challenge':
            challenge = random.randint(0, 2**32 - 1)
            print(f"Challenge value: {hex(challenge)}")
            chal_data = struct.pack("!I",challenge)
            print(f"Challenge bytes:  {chal_data.hex(' ')}")
            client_socket.sendall(chal_data)
    
        # Receive 16 bytes from the client
        #cmd_data = client_socket.recv(16)
        cmd_data = receive_exact_bytes(client_socket,16) # wait for receipt of full 16 bytes (allows multiple packets to work)
        print(f"Command received:  {cmd_data.hex(' ')}")
        
        if mode=='encrypt' or mode=='challenge':
            cmd_data = aes_decrypt(GLOBAL_KEY,cmd_data)
            print(f"Command decrypted: {cmd_data.hex(' ')}")
        
        try:
            cmd = Command.from_bytes(cmd_data)
            print(f"Processing {cmd}")
            if mode=='challenge' and cmd.challenge != challenge:
                print(f"I provided challenge value {hex(challenge)}, but I got back wrong challenge value {hex(cmd.challenge)}, rejecting command.")
                resp = Response(0)
            elif cmd.verb==0:
                print(f"LED: \033[32mOFF\033[m")
                resp = Response(1)
            elif cmd.verb==1:
                print(f"LED: \033[42;97mON\033[m")
                resp = Response(1)
            else:
                print(f"Invalid verb: {cmd.verb}")
                resp = Response(0)
        except ValueError as e:
            print(e)
            resp = Response(0)
        
            
        # Send the response to the client
        resp_data = resp.to_bytes()
        print(f"Response generated: {resp_data.hex(' ')}")
        if mode=='encrypt' or mode=='challenge':
            resp_data = aes_encrypt(GLOBAL_KEY,resp_data)        
            print(f"Response encrypted: {resp_data.hex(' ')}")
        client_socket.sendall(resp_data)
    finally:
        # Close the connection
        client_socket.close()

def handle_client_connection(port, mode):
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
            handle_service(client_socket, mode)
    except KeyboardInterrupt:
        print(f"Server on port {port} shutting down...")
    finally:
        # Close the server socket
        server_socket.close()
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pymed server: receive and process requests to turn a virtual LED on or off.")
    
    # Add arguments
    parser.add_argument("port", type=int, help="Port number to listen")
    parser.add_argument("-m", "--mode", choices=["basic", "encrypt", "challenge"], default="basic", help="Protocol mode: 'basic' (default), 'encrypt', or 'challenge'")

    args = parser.parse_args()
    
    handle_client_connection(args.port, args.mode)
    
