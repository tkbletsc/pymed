#!/usr/bin/python3

# provided library for Command and Response (like the arduino code), plus AES functions
from pymed_protocol import Command,Response,aes_encrypt,aes_decrypt

############ Making a command, converting to bytes #################

# make a command with verb 1 (LED on)
cmd = Command(1)
print(f"cmd: {cmd}")

# convert it to bytes suitable for sending over a socket
cmd_data = cmd.to_bytes()
print(f"cmd_data: {cmd_data} ({cmd_data.hex(' ')})") # print both as a plain byte string and as hex
print("")


############ Parsing a response from given bytes (and succeeding) #################


# suppose someone gives us these bytes, perhaps from a socket
resp_data = bytes.fromhex("53 4c 41 56 01 00 00 00 00 00 00 00 00 00 00 00")
print(f"Someone gave me these bytes: {resp_data} ({resp_data.hex(' ')})")

# you can turn them into a Response object using its from_bytes method
# this constructor checks that the input data is the right length and has the right magic, and raises a ValueError if not
try:
    resp = Response.from_bytes(resp_data)
    print(f"Parsed bytes as a valid response: {resp}")
except ValueError as e:
    print(f"Unable to parse those bytes as a valid response: {e}")
print("")


############ Parsing a response from given bytes (and failing) #################


# let's try that again, but suppose the magic isn't right
resp_data = bytes.fromhex("88 77 66 44 01 00 00 00 00 00 00 00 00 00 00 00")
print(f"Someone gave me these CURSED bytes: {resp_data} ({resp_data.hex(' ')})")

# let's try to parse it as a Response, but the exception will be triggered instead
try:
    resp = Response.from_bytes(resp_data)
    print(f"Parsed bytes as a valid response: {resp}")
except ValueError as e:
    print(f"Unable to parse those bytes as a valid response: {e}")
print("")


######### Encryption and decryption ######################

example_key = b'0123456789abcdef' # must be 16 bytes
wrong_key = b'9999999999999999'

plaintext = b'I have 16 bytes.' # also must be 16 bytes
print(f"Plaintext:  {plaintext.hex(' ')} ({plaintext})")

ciphertext = aes_encrypt(example_key, plaintext)
print(f"Ciphertext: {ciphertext.hex(' ')}")

decrypted_plaintext = aes_decrypt(example_key, ciphertext)
print(f"Decrypted:  {decrypted_plaintext.hex(' ')} ({decrypted_plaintext})")

bad_decrypted_plaintext = aes_decrypt(wrong_key, ciphertext)
print(f"Wrong key:  {bad_decrypted_plaintext.hex(' ')} < unreadable junk!")

