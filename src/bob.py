import os, socket, random

# Bob: store chunks into a file

class bob:
    
    def __init__(self, self_infos:tuple, tracker_infos:tuple) -> None:
        self.host, self.port = self_infos
        self.tracker_host, self.tracker_port = tracker_infos
        
    """
        name: get_participants
        debrief: connect to the tracker and get the list of participants
        return: participants_info (list) 
    """
    def get_participants(self) -> list:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.connect((self.tracker_host, self.tracker_port))
            s.sendall(b"GET_PARTICIPANTS")
            data = s.recv(1024)
        
        if not data:
            return []
        
        participants = data.decode().split("\n")
        
        participants_info = []
        
        for participant in participants:
            try:
                host, port = participant.split(":")
            except ValueError:
                print(f"Invalid participant: {participant}")
                continue
            participants_info.append({"host": host, "port": int(port)})
        return participants_info # servers ip:port 
    
    """
        name: store_chunks
        param: chunks (list)
        debrief: store chunks into a choosen file
    """    
    def store_chunks(self, chunks:list, file_name:str="file.txt") -> None:

        if not os.path.exists("files"):
            os.makedirs("files")
        
        file_path = os.path.join("files", file_name)
        with open(file_path, 'w') as file:
            for chunk in chunks:
                if chunk:
                    file.write(str(chunk))
                else:
                    print("Empty file")
        
        print("File successfully saved")
    
    """
        name: start
        debrief: start the download
    """   
    def start(self) -> None:
        
        participants = self.get_participants()
        if not participants:
            print("No participants")
            return
        
        print(f"Participants:", "\n".join([f"{p['host']}:{p['port']}" for p in participants]))

        """
            name: get_chunk
            param: participant (dict), c_id (int)
            debrief: get a chunk from a participant
            return: c_id (int), chunk (str)
        """
        def conn_n_get(c_id:int, s:object) -> tuple:
                
            s.sendall(b"GET_CHUNK " + str(c_id).encode())
            data = s.recv(1024)
            s.sendall(b'OK')
            
            if not data:
                return None
            # data  = b'Hello world'
            chunk = data.decode()
            return (c_id, chunk)
        
        print("Participant selected for the file length: ", participants[0])
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = random.randint(6666, 8888)
        s.connect((participants[0]["host"], participants[0]["port"]))
        s.sendall(b"GET_FILE_LENGTH")
        self.file_length = int(s.recv(1024).decode())
        s.close()
        
        print("File length:", self.file_length)
        
        chunks = [None for i in range(int(self.file_length/1024)+1)]
        
        connections = {}

        #threads = []
        
        # get chunks
        for i in range(len(chunks)):
            if chunks[i]:
                continue
            
            x = random.randint(0, len(participants)-1)
            
            if x not in connections:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((participants[x]["host"], participants[x]["port"]))
                connections[x] = s
                
            print("Getting chunk", i)
            try:
                chunks[i] = conn_n_get(i, connections[x])[1]
            except Exception as e:
                print(e)
        
        print("Chunks received")
        
        print("Storing chunks...")
        
        self.store_chunks(chunks)
        return
        
if __name__ == "__main__":
    B = bob(("localhost", random.randint(6666,8888)), ("localhost", 6881)) # (host, port of himself), (tracker_host, tracker_port)
    B.start()