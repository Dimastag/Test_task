import serial
import time

command_list = {'GET_A': ['A', '_', '10V'], 'GET_B': ['B', '_', '5V'], 'GET_C': ['C', '_', '10A']}

def send_data(ser, data):
    ser.write(data.encode())


ser = serial.Serial("COM2", 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=1)
while True:
    request = ser.read(10).decode().strip()
    if request:
        if request in command_list:
            response_data = ''.join(command_list[request])
            send_data(ser, response_data)
            print("Отправлен ответ на запрос", request)
        else:
            print("Неизвестный запрос:", request)
            send_data(ser, ".")
            break
    time.sleep(0.1)