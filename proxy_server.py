#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
GOOGLE_HOST = "google.com"
GOOGLE_PORT = 80
PROXY_SERVER_HOST = ""
PROXY_SERVER_PORT = 8080
BUFFER_SIZE = 512

def handle_process(conn, addr, proxy_end):
    #recieve data from client
    full_data = conn.recv(BUFFER_SIZE)
    print("Data from Client to Proxy_Server:", full_data)
    #send data to google
    proxy_end.sendall(full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    full_data = proxy_end.recv(BUFFER_SIZE)
    print("Data from Google to Proxy_Server:", full_data)
    conn.send(full_data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Proxy_Server Connected by", addr)
           
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                 #connect to google.com
                GOOGLE_IP = socket.gethostbyname(GOOGLE_HOST)
                proxy_end.connect((GOOGLE_IP , GOOGLE_PORT))
                p = Process(target=handle_process, args=(conn, addr, proxy_end))
                p.daemon = True
                p.start()
                
                time.sleep(0.5)
            conn.close()

if __name__ == "__main__":
    main()
