import socketserver

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class ClientHandler(socketserver.BaseRequestHandler):

    def handle(self):

        encrypted_key = self.request.recv(1024).strip() # get encrypted key
        print(f'\n---\n[*] Recieved encrypted key: {encrypted_key}') # print encrypted key
        
        with open('private.key', 'rb') as pkf: # we read the private key for further using
            private_key = serialization.load_pem_private_key(
                pkf.read(),
                password = None,
                backend = default_backend()
            )

        try:
            print(f'\n[*] Decrypting encrypted key {encrypted_key} ...') 

            decrypted_key = private_key.decrypt( # decrypt key from user
                encrypted_key,
                padding.OAEP(
                    mgf = padding.MGF1( algorithm = hashes.SHA256()), # use OAEP algorithm and SHA256 hashing algorithm
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )

            print(f'\n[*] Decrypted key: {decrypted_key}')
            self.request.sendall(decrypted_key)

        except Exception as e:
            print(f'\n[OOPS...] Error while decryption: {e}')
            self.request.sendall(b'[OOPS...] Error while decryption') # send message



if __name__ == '__main__':
    HOST, PORT = '', 8000 # use init IP, port 8000 
    tcpServer = socketserver.TCPServer((HOST, PORT), ClientHandler) # server init
    
    try:

        print(f'[*] Server is running.\n\n[+] HOST: {HOST}\n[+] PORT: {PORT}')
        tcpServer.serve_forever()

    except KeyboardInterrupt:

        print('\n[*] Server was stopped by user')
        tcpServer.server_close()

    except Exception as e:

        print(f'[OOPS...] Error: {e}')
        tcpServer.server_close()
