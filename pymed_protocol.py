import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def aes_encrypt(key, data):
    # Ensure the key length is appropriate for AES-128 (16 bytes)
    if len(key) != 16:
        raise ValueError("Key length must be 16 bytes for AES-128")

    # Ensure the data length is appropriate for AES block size (16 bytes)
    if len(data) != 16:
        raise ValueError("Data length must be 16 bytes for AES encryption")

    # Create an AES cipher object with the specified key using ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Perform AES encryption
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return encrypted_data

def aes_decrypt(key, encrypted_data):
    # Ensure the key length is appropriate for AES-128 (16 bytes)
    if len(key) != 16:
        raise ValueError("Key length must be 16 bytes for AES-128")

    # Ensure the data length is appropriate for AES block size (16 bytes)
    if len(encrypted_data) != 16:
        raise ValueError("Data length must be 16 bytes for AES encryption")
        
    # Create an AES cipher object with the specified key using ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Perform AES decryption
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data

class Command(object):
    expected_magic = b'MIRO'
    def __init__(self,verb,challenge=0):
        self.verb = verb
        self.challenge = challenge # this will be used for challenge mode. you can ignore it if you're not doing challenge mode yet
    
    def to_bytes(self):
        # 4 byte magic "MIRO"
        # 2 byte verb
        # 4 byte challenge int
        # 6 bytes padding
        return struct.pack('!4shI6x', self.expected_magic, self.verb, self.challenge)
        
    @staticmethod
    def from_bytes(buf):
        if len(buf) != 16:
            raise ValueError(f"Wrong packet length: {len(buf)}")
        magic,verb,challenge = struct.unpack('!4shI6x', buf)
        if magic != Command.expected_magic:
            raise ValueError(f"Wrong magic: {magic.hex(' ')}, expected {Command.expected_magic.hex(' ')}")
        return Command(verb,challenge)
    
    def __str__(self):
        return f"Command({self.verb})"

class Response(object):
    expected_magic = b'SLAV'
    def __init__(self,result):
        self.result = result
    
    def to_bytes(self):
        # 4 byte magic "SLAV"
        # 1 byte result
        # 11 bytes padding
        return struct.pack('!4sB11x', self.expected_magic, self.result)
        
    @staticmethod
    def from_bytes(buf):
        if len(buf) != 16:
            raise ValueError(f"Wrong packet length: {len(buf)}")
        magic,result = struct.unpack('!4sB11x', buf)
        if magic != Response.expected_magic:
            raise ValueError(f"Wrong magic: {magic.hex(' ')}, expected {Response.expected_magic.hex(' ')}")
        return Response(result)
    
    def __str__(self):
        return f"Response({self.result})"