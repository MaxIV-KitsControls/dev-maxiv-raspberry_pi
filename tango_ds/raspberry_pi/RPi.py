"""
Class for the Raspberry Pi Tango device server GPIO control.
Class has no Tango dependence.
2018-04-03.
"""


import socket
import sys

class Raspberry:


    def __init__(self, host):
        self.host = host
        self.port = 9788
        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)

    def connect_to_pi(self):
        self.sock.connect((self.host, self.port))

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            return None

    def query(self, cmd):
        self.sock.sendall((cmd).encode())
        val = str(self.sock.recv(1024))
        val = val.replace("'","").replace("b","")
        bol = self.str_to_bool(val)
        return bol

    def readvoltage(self, pin):
        cmd = str(pin) + ' READVOLTAGE'
        return self.query(cmd)

    def readoutput(self, pin):
        cmd = str(pin) + ' READOUTPUT'
        return self.query(cmd)

    def setvoltage(self, pin, value):
        cmd = str(pin) + ' SETVOLTAGE ' + str(value)
        return self.query(cmd)

    def setoutput(self, pin, value):
        data = str(pin) + ' SETOUTPUT ' + str(value)
        self.sock.sendall((data).encode())

    def start_motor(self):
        data = 'X MOTOR True'
        self.sock.sendall((data).encode())

    def stop_motor(self):
        data = 'X MOTOR False'
        self.sock.sendall((data).encode())

    def resetall(self):
        data = 'ALL RESET'
        self.sock.sendall((data).encode())

    def turnoff(self):
        data = 'ALL OFF'
        self.sock.sendall((data).encode())

    def disconnect_from_pi(self):
        self.sock.close()
