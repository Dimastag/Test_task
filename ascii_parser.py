import serial
import serial.tools.list_ports
import socket


class AsciiParser:
    """Класс для взаимодействия с COM портами"""

    def __init__(self, com, baund):
        self.port = com
        self.baund = baund

    def sender_receiver(self, command):
        """
        Функция для взаимодействия с устройством через COM порт
        :param command:  Запрос к устройству, например GET_A
        """
        try:
            ser = serial.Serial(self.port, self.baund, bytesize=serial.EIGHTBITS, parity=serial.PARITY_ODD,
                                stopbits=serial.STOPBITS_ONE, timeout=1)
            ser.write(command.encode(encoding='utf-8'))  # Отправка команды

            response = ser.read(100).decode("ascii")  # Чтение ответа
            print(f'Данные с устройства: {response}')

        except Exception as e:
            print('Error:', e)


class TcpAsciiParser:
    """Класс для взаимодействия с TCP на базе сокетов"""

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket()

    def sockets(self, command):
        """
         Функция для взаимодействия с устройством через TCP
        :param command: Запрос к устройству, например GET_A
        """
        self.sock.connect((self.address, self.port))
        self.sock.send(command.encode(encoding='utf-8'))

        data = self.sock.recv(1024).decode("ascii")
        self.sock.close()

        print(data)


if __name__ == "__main__":
    # parser = AsciiParser('COM1', 9600)
    # parser.sender_receiver('GET_A')
    parser = TcpAsciiParser('localhost', 10000)
    parser.sockets('GET_C')
