import socket 
import random 

# alice : send chunks to participants

class Alice:
    def __init__(self, host: tuple, tracker: tuple):
        self.host, self.port = host
        self.tracker_host, self.tracker_port = tracker

    def new_participant(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.tracker_host, self.tracker_port))
            msg = b"NEW_PARTICIPANT " + str(self.port).encode()
            s.sendall(msg)
            print(msg)
            print("You are now participating in the download")

    def create_chunks(self, file_path: str, chunk_size: int):
        chunks = []
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
        print(f"{len(chunks)} chunks created")
        return chunks

    def send_chunk(self, s: object, chunk: str):
        data = chunk
        s.sendall(data)
        data = s.recv(1024)
        if data != b'OK':
            raise RuntimeError('Server did not confirm reception of data')

    def share_file(self, chunks: list):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            print("[i] Your addr is " + str(self.host) + ":" + str(self.port))
            print("Waiting for a connection...")
            while True:
                
                conn, addr = s.accept()
                
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    elif b"GET_CHUNK" in data:
                        c_id = int(data.split(b" ", 1)[1])
                        chunk = chunks[c_id]
                        self.send_chunk(conn, chunk)
                    elif data == b"GET_FILE_LENGTH":
                        conn.sendall(str(len(open(file_path, 'rb').read())).encode())
                    else:
                        print("Unknown command")
                        break
                        
    def handle_interrupt(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.tracker_host, self.tracker_port))
            p = self.port
            msg = f"RM_PARTICIPANT {p}"
            s.sendall(msg.encode())
            s.close()

if __name__ == "__main__":
    port = random.randint(6000, 50000)
    
    host = ("localhost", port)
    
    tracker = ("localhost", 6881)

    A = Alice(host, tracker)
    A.new_participant()

    try:
        file_path = "../documents/lorem.txt"
        chunk_size = 1024  # with lorem.txt, 10 chunks of 1024 bytes
        chunks = A.create_chunks(file_path, chunk_size)
        A.share_file(chunks)
    except (KeyboardInterrupt, Exception) as e:
        if e:
            print(e)
        if KeyboardInterrupt:
            A.handle_interrupt()
        print("Exiting...")
        exit()