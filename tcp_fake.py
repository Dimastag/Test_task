import socket
import time

command_list = {'GET_A': ['A', '_', '10V'], 'GET_B': ['B', '_', '5V'], 'GET_C': ['C', '_', '10A']}


server_address = ('localhost', 10000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)

print("Ждем соединения...")
client_socket, client_address = server_socket.accept()
print(f"Получено соединение от {client_address}")

def send_data(client_socket, data):
    client_socket.sendall(data.encode())


while True:
    request = client_socket.recv(100).decode().strip()
    if request:
        if request in command_list:
            response_data = ''.join(command_list[request])
            send_data(client_socket, response_data)
            print("Отправлен ответ на запрос", request)
        else:
            print("Неизвестный запрос:", request)
            send_data(client_socket, ".")
            break
    time.sleep(0.1)

client_socket.close()



