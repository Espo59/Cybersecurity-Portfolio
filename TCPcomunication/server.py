import socket

# Define the server's IP address and the port to listen on
# Empty string means it will listen on all available network interfaces
ip = "" 
port = 4444

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)

    # Bind the socket to the address and port
    sock.bind(address)
    
    # Start listening for incoming connections (1 specifies the backlog of connections)
    sock.listen(1)
    print(f"---------listening for connection on port-----------{port}")

    # Accept a new connection
    # conn is a new socket object usable to send and receive data
    # ipvictim is the address bound to the socket on the other end of the connection
    conn, ipvictim = sock.accept()
    print(f"Connection established with {ipvictim}")

    # Message to be sent to the connected client
    msg = "this is the message from the server"
    
    # Send the encoded message (strings must be converted to bytes)
    conn.send(msg.encode())

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
