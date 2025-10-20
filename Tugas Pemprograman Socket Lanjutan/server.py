import socket
from threading import Thread
print("Server dimulai...")


listenerSocket = socket.socket()
serverIP = "0.0.0.0"
serverPort = 2222
clients = []  # simpan semua client

def kirim_pesan(handlerSocket: socket.socket):
    while True:
        try:
            message = input()
            # kirim ke semua client
            for client in clients:
                try:
                    client.send(f"server: {message}".encode())
                except:
                    print("[!] gagal kirim ke salah satu client.")
            print("server: {} ".format(message))
        except:
            print("[!] error waktu kirim pesan.")
            break

def terima_pesan(handlerSocket: socket.socket, addr):
    while True:
        try:
            message = handlerSocket.recv(1024)
            if not message:
                print(f"[!] client {addr} terputus.")
                clients.remove(handlerSocket)
                handlerSocket.close()
                break
            text = message.decode('utf-8')
            print("client {}: {}".format(addr, text))
            # broadcast ke semua client lain
            for client in clients:
                if client != handlerSocket:
                    client.send(f"client {addr}: {text}".encode())
        except:
            print(f"[!] error waktu nerima pesan dari {addr}.")
            if handlerSocket in clients:
                clients.remove(handlerSocket)
            handlerSocket.close()
            break

listenerSocket.bind((serverIP, serverPort))
listenerSocket.listen(5)
print("[+] Server jalan di {}:{}".format(serverIP, serverPort))
print("[+] Menunggu koneksi dari client...")

try:
    while True:
        handlerSocket, addr = listenerSocket.accept()
        clients.append(handlerSocket)
        print("[+] Terhubung dengan client dari alamat: {}".format(addr))

        thread_terima = Thread(target=terima_pesan, args=(handlerSocket, addr))
        thread_terima.start()

        # thread kirim server cuma dijalankan sekali (biar gak numpuk)
        if len(clients) == 1:
            thread_kirim = Thread(target=kirim_pesan, args=(handlerSocket,))
            thread_kirim.start()

except KeyboardInterrupt:
    print("\n[!] Server dimatikan manual.")
    for c in clients:
        c.close()
    listenerSocket.close()
