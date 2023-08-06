################################################

# Creator: Hunter Mikesell
# Version: 1.0.L
# LIC: MIT

################################################

from os import system as run

from platform import system as os_name

import http.server# type: ignore
import http.client# type: ignore
import _socket# type: ignore
import socket# type: ignore

import os


if os.path.exists("InstalledPkgs.txt"):
    pass
else:
    print(str("Installing Packages: ['time', 'random', 'colorama', 'requests']"))
    if os_name == str("Windows"):
        run("python -m pip install time")
        run("python -m pip install random")
        run('python -m pip install colorama')
        run('python -m pip install requests')
    with open("InstalledPkgs.txt", 'w') as fw:
        fw.write("True")
        fw.close()

__import__("colorama").init()

print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Netstock{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {__import__("colorama").Fore.CYAN}Thanks for using Netstock, Have a nice day :){__import__("colorama").Fore.RESET}')

class TCPServerException(Exception):
    pass

class TCPServerSocketError(_socket.error):
    pass

class IndentError(IndentationError):
    pass

class Warning(Warning):
    pass

class AtrributeErr(AttributeError):
    pass

def useSystemIP():
    try:
        return socket.gethostbyname(socket.gethostname())
    except TCPServerException as EX8:
        print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX8}')
    except TCPServerSocketError as SErr8:
        print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr8}')

def genRandomPort():
    return __import__('random').randint(5, 6000)

class TCPserver(object):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server = socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    
    def create(self):
        try:
            self.server.bind((str(self.host), int(self.port)))
        except TCPServerSocketError as SErr:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr}')
        except TCPServerException as EX:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX}')

    def start_listener(self, max_connections: int = 1):
        try:
            self.server.listen(max_connections)
        except TCPServerException as EX2:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX2}')
        except TCPServerSocketError as SErr2:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr2}')

    def accept_all(self):
        try:
            self.Client, self.Addr = self.server.accept()
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Accepted Connection{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: ({__import__("colorama").Fore.MAGENTA}{self.Addr[0]}{__import__("colorama").Fore.RESET}:{__import__("colorama").Fore.BLUE}{self.Addr[1]}{__import__("colorama").Fore.RESET})')
        except TCPServerException as EX1:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX1}')
        except TCPServerSocketError as SErr1:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr1}')

    def getClientAddress(self):
        try:
            Address = self.Addr[0]
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Addr{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {Address}')
        except TCPServerException as EX3:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX3}')
        except TCPServerSocketError as SErr3:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr3}')

    def getClientPort(self):
        try:
            clientPort = self.Addr[1]
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Port{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {clientPort}')
        except TCPServerException as EX4:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX4}')
        except TCPServerSocketError as SErr4:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr4}')
    
    def recv_bytes(self):
        try:
            recv_all = self.Client.recv(1024).decode()
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Recieved{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {recv_all}')
        except TCPServerException as EX5:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX5}')
        except TCPServerSocketError as SErr5:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr5}')

    def send_bytes(self, DATA: str) -> None:
        try:
            self.Client.send(str(DATA).encode())
        except TCPServerException as EX6:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX6}')
        except TCPServerSocketError as SErr6:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr6}')
    
    def getHost_info(self):
        try:
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}IP: {__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {socket.gethostbyname(socket.gethostname())}')
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}OS: {__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {os_name()}')
            loginInfo = __import__('os').getlogin()
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Login: {__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {loginInfo}')
        except TCPServerException as EX7:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX7}')
        except TCPServerSocketError as SErr7:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr7}')

    def close_server(self):
        try:
            self.server.close()
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Server{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {__import__("colorama").Fore.CYAN}Closed Server{__import__("colorama").Fore.RESET}')
        except TCPServerException as EX9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX9}')
        except TCPServerSocketError as SErr9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr9}')

    def disconnect_client(self):
        try:
            self.server.close()
            print(f'{__import__("colorama").Fore.MAGENTA}[{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.BLUE}Client{__import__("colorama").Fore.RESET}{__import__("colorama").Fore.MAGENTA}]{__import__("colorama").Fore.RESET}: {__import__("colorama").Fore.CYAN}Disconnected Client{__import__("colorama").Fore.RESET}')
        except TCPServerException as EX9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX9}')
        except TCPServerSocketError as SErr9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr9}')

class TCPClient(object):
    def __init__(self) -> None:
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    
    def connectToServer(self, host: str, port: int):
        try:
            self.server.connect((host, port))
        except TCPServerException as EX9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX9}')
        except TCPServerSocketError as SErr9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr9}')

    def sendMsg(self, data: str):
        try:
            self.server.send(data.encode())
        except TCPServerException as EX9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX9}')
        except TCPServerSocketError as SErr9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr9}')

    def recv_data_from_server(self, buff_size: int):
        try:
            return self.server.recv(buff_size).decode()
        except TCPServerException as EX9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {EX9}')
        except TCPServerSocketError as SErr9:
            print(f'[{__import__("colorama").Fore.RED}Error{__import__("colorama").Fore.RESET}]: {SErr9}')

def set_timeout(seconds: int):
    for _ in range(seconds):
        __import__("time").sleep(1)