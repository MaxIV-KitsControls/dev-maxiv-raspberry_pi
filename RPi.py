"""
Class for the Raspberry Pi Tango device GPIO control
Sends encoded string to Raspberry Pi TCP/IP server
Class has no Tango dependence
Sundberg, 2018-03-06
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
        
    def readvoltage(self, pin):
        data = str(pin) + ' READVOLTAGE'
        print(data)
        self.sock.sendall((data).encode())
        val = self.sock.recv(1024)
        val = str(val).replace("b","")
        val = str(val).replace("'","")
        bol = self.str_to_bool(val)
        return bol
        
    def setvoltage(self, pin, value):
        data = str(pin) + ' SETVOLTAGE ' + str(value)
        print(data)
        self.sock.sendall((data).encode())
    
    def readoutput(self, pin):
        data = str(pin) + ' READOUTPUT'
        print(data)
        self.sock.sendall((data).encode())
        val = self.sock.recv(1024)
        val = str(val).replace("b","")
        val = str(val).replace("'","")
        bol = self.str_to_bool(val)
        return bol
        
    def setoutput(self, pin, value):
        data = str(pin) + ' SETOUTPUT ' + str(value)
        print(data)
        self.sock.sendall((data).encode())
        
    def resetall(self):
        data = 'ALL RESETALL'
        print(data)
        self.sock.sendall((data).encode())
        
    def turnoff(self):
        data = 'ALL OFF'
        print(data)
        self.sock.sendall((data).encode())
        
    def disconnect_from_pi(self):
        self.sock.close()


