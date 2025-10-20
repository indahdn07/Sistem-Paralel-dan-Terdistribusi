import socket
from threading import Thread

connectionSocket = socket.socket()
serverIP = "127.0.0.1"
serverPort = 2222

def kirim_pesan(handlerSocket : socket.socket):
    while True:
        try:
            message = input()
            handlerSocket.send(message.encode())
            print("client: {} ".format(message))
        except:
            print("[!] gagal kirim, mungkin koneksi putus.")
            break

def terima_pesan(handlerSocket : socket.socket):
    while True:
        try:
            message = handlerSocket.recv(1024)
            if not message:
                print("[!] server terputus.")
                break
            print("server: {} ".format(message.decode('utf-8')))
        except:
            print("[!] error waktu nerima pesan.")
            break

try:
    connectionSocket.connect((serverIP, serverPort))
    print("[+] Terhubung dengan server di {}:{}".format(serverIP, serverPort))
except:
    print("[!] gak bisa konek ke server.")
    exit()

thread_kirim = Thread(target=kirim_pesan, args=(connectionSocket,))
thread_terima = Thread(target=terima_pesan, args=(connectionSocket,))

thread_kirim.start()
thread_terima.start()

thread_kirim.join()
thread_terima.join()
