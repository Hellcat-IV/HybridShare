import socket, datetime

# Tracker : Store and share participant list

def get_time() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

class Tracker:
    
    def __init__(self, host:str, port:int) -> None:
        
        self.host = host
        self.port = port
        self.participants = []

    """
        name: start
        debrief: waiting for connections and send participants lists if the request is GET_PARTICIPANTS
    """
    def start(self) -> None:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.bind((self.host, self.port))
            s.listen(1)
            
            print(f"{get_time()} - Waiting for new connections ({self.host}:{self.port})\n")

            while True:
                try:
                    conn, addr = s.accept()
                    print(f"Etablished connection with {str(addr[0])}:{str(addr[1])}:\n")
                    
                    data = conn.recv(1024)
                    
                    if data == b"GET_PARTICIPANTS":
                        print(get_time(), "- GET_PARTICIPANTS FROM", str(addr[0]), str(addr[1]) + "\n")
                        self.get_participants(conn)
                        
                    elif b"NEW_PARTICIPANT" in data:
                        ip = addr[0]
                        port = int(data.split(b" ", 1)[1])
                        print(get_time(), "- NEW_PARTICIPANT FROM", str(ip), str(port) + "\n")
                        self.new_participant(ip, port)
                        
                    elif b"RM_PARTICIPANT" in data:
                        ip = addr[0]
                        port = int(data.split(b" ", 1)[1])
                        print(get_time(), "- RM_PARTICIPANT FROM", str(ip), str(port) + "\n")
                        self.rm_participant(ip, port)
                        
                    conn.close()
                    
                except Exception as e:
                    print(f"Error: {e} | on line {e.__traceback__.tb_lineno}\n")

    """
        name: get_participants
        param: conn (socket connetion)
        debrief: send participants lists to the client
    """
    def get_participants(self, conn:object) -> None:

        participants = "\n".join(self.participants)
        conn.sendall(participants.encode())

    """
        name: new_participant
        param: host
        param: port
        debrief: add a new participant to the list
    """
    def new_participant(self, host:str, port:int) -> None:

        participant = f"{host}:{port}"
        self.participants.append(participant)

    """
        name: rm_participant
        param: host
        param: port
        debrief: remove a participant from the list
    """
    def rm_participant(self, host:str, port:int) -> None:

        participant = f"{host}:{port}"
        self.participants.remove(participant)


if __name__ == "__main__":

    tracker = Tracker("localhost", 6881)
    tracker.start()