# pymed

A codebase for students to study basic encryption and challenge response using Python code similar to what you'd find in an embedded device. Packets are 16 bytes, and encryption/decryption primitives are provided.

For a full intro, see this video: https://youtu.be/2y9doohWGyc 

Files:
 - **pymed_protocol.py**: Provided library with Command and Response classes and cryptography primitives
 - **example-protocol-stuff.py**: Example usage of pymed_protocol
 - **example-server.py**, **example-client.py**: Example server and client code that just sends "ping" and "pong" back and forth
 - **pymed-server.py**: The provided pymed server which listens for clients, accepts a Command, turns on/off a virtual "LED" based on the command, and sends a Response. Includes optional modes for encryption and challenge/response.
 - **pymed-client.py**: (Not included) This is the program the student will be writing.

## Assignments
 1. Write a basic pymed-client.py that sends a Command with a verb specified on the command line, receives and parses a Response, and displays it. Test this client against the provided server. The intro video will get you started.
 2. Using Wireshark, observe the traffic between pymed-client and pymed-server. You can see everything! Using just a terminal and netcat, construct a command that will maliciously turn on the LED. Hints:
      - ``echo -e '\x55\x44'`` will create the bytes 55 44
      - ``nc localhost 5000`` will connect to the given host and port, and you can pipe content in and out of it
      - ``hd`` or ``hexdump -C`` will display output as formatted hex
 3. Update your pymed-client to use encryption. Encrypt your command before sending it, and decrypt the response before parsing it. Run the server with the option "-m encrypt". Note the global secret key in the provided server. Once successful, your client and server should work as before, but with encryption. 
      - Hint: **pymed_protocol.py** includes ``aes_encrypt`` and ``aes_decrypt``, which operate on 16-byte blocks. Commands and responses are also 16 bytes.
 4. Again using wireshark, we see that we cannot understand the content of packets, *however*, we observe that the packets are always the same, because the key and command content is always the same! This means our protocol is vulnerable to *replay attacks*, in which the attacker blindly sends an identical packet. Observe the sequence of bytes that correspond to LED ON in wireshark, then construct an attack on the terminal that replays this request and confirm that it indeed turns the LED on, despite the attacker not knowing the secret key.
 5. Augment your pymed-client with support for a more detailed challenge/response protocol. Now, upon connecting to the server in "-m challenge" mode, the server will send you a random 4 byte integer called the *challenge*. You must include this integer in the challenge field of your command before encrypting and sending it. The Command object supports an optional challenge argument for this purpose. Once successful, this will make every command look entirely different, as the encrypted challenge will change the rest of the ciphertext entirely.
 6. Now observe the traffic in Wireshark. Attempt to perform a replay attack, and observe that you are unsuccessful. 
