# RFC Documentation: File Sharing Protocol

Authors:
- [CalValmar](https://github.com/CalValmar)
- [Kenoor](https://github.com/bxsic-fr)

## Abstract

This document describes a file sharing protocol that enables users to share and download files in a decentralized manner. The protocol involves three main components: Alice, Bob, and the Tracker. Alice is responsible for sharing file chunks, Bob is responsible for downloading and storing the file, and the Tracker keeps track of the participants in the network.

## 1. Introduction

The file sharing protocol allows users to distribute large files across multiple participants in a decentralized network. It aims to provide efficient and reliable file transfer while ensuring data integrity.

## 2. Protocol Overview

The protocol involves the following steps:

2.1. Alice, the file sharer, registers as a participant by sending a `NEW_PARTICIPANT` request to the Tracker, providing her machine's IP and port.

2.2. Alice creates file chunks of a fixed size, typically 1024 bytes, to divide the file into manageable pieces.

2.3. Bob, the file downloader, connects to the Tracker and requests the list of participants using a `GET_PARTICIPANTS` request.

2.4. Bob obtains the file size by sending a `GET_FILE_LENGTH` request to the first participant in the list received from the Tracker.

2.5. Bob creates an empty list to store the file chunks, with the length determined by dividing the file size by the chunk size.

2.6. Using a threaded system, Bob sends `GET_CHUNK` requests to the participants to retrieve the corresponding file chunks. If an error occurs, a new attempt is made at the end.

2.7. Bob saves the received chunks in a file, reconstructing the original file.

```
 +-----------------+
 |                 |
 |       Alice     |
 |                 |
 +-----------------+
          |
          |      +-----------------+
          +----> |    Tracker      |
                 |                 |
                 +-----------------+
                          |
                          |     +-----------------+
                          +---> |       Bob       |
                                |                 |
                                +-----------------+
```


## 3. Detailed Protocol Description

3.1. Alice's Responsibilities

Alice initiates the file sharing process by registering as a participant and sharing file chunks upon request. She uses a TCP socket connection to communicate with the Tracker and other participants. Alice also handles potential interruptions and gracefully exits the protocol.

3.2. Bob's Responsibilities

Bob initiates the file download process by connecting to the Tracker, obtaining the list of participants, and retrieving file chunks from them. He uses TCP socket connections to communicate with the Tracker and other participants. Bob ensures the successful retrieval of all file chunks and stores them into a file.

3.3. Tracker's Responsibilities

The Tracker acts as a central entity in the protocol. It receives requests from participants and provides them with the necessary information. It maintains a list of participants and handles new participant registrations and participant removals.

## 4. Communication Protocol

4.1. Participants' Communication with the Tracker

Participants communicate with the Tracker using predefined request messages:
- `NEW_PARTICIPANT` to register as a new participant.
- `GET_PARTICIPANTS` to obtain the list of participants.

4.2. Participants' Communication with Each Other

Participants communicate with each other using predefined request messages:
- `GET_CHUNK` to request a specific file chunk.
- `GET_FILE_LENGTH` to request the length of the file.

4.3. Removal of a Participant

To remove a participant from the network, the following request message is used:
- `RM_PARTICIPANT` to indicate the removal of a participant.

## 5. Performance Optimization

To optimize performance, participants use threaded connections to retrieve file chunks in parallel. Additionally, the protocol divides files into smaller chunks, allowing for concurrent retrieval and efficient distribution.

## 6. Security Considerations

This protocol focuses on file sharing and does not include advanced security features. It is recommended to use additional encryption and authentication mechanisms to secure the file transfer process.

## 7. Future Enhancements

Potential future enhancements for the file sharing protocol include:
- Adding support for file integrity verification using checksums.
- Implementing authentication and access control mechanisms.
- Supporting encryption for secure file transfers.

## 8. Conclusion

The file sharing protocol described in this document enables efficient and decentralized file distribution among participants. By dividing files into chunks and utilizing parallel retrieval, the protocol enhances file transfer speed and reliability.
