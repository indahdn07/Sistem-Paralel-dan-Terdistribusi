import socket

def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server mulai di port 8080. menunggu koneksi...")

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode("utf-8")
        print(f"menerima pesan dari klien: {data}")
        
        client_socket.send("Hello dari server!".encode("utf-8"))
        client_socket.close()

if __name__ == " _main_":
    start_server()