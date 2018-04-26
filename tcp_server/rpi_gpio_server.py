"""
TCP Server for the RPi GPIO tango device server.
2018-04-03.
"""

import socket
import socketserver
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class TCP(socketserver.BaseRequestHandler):
    

    def handle(self):
        self.request.settimeout(5)
        print("Client connection: {}".format(self.client_address[0]))
        while True:
            try:
                data = self.request.recv(1024).strip()
                if not data:
                    break
                print("{} wrote:".format(self.client_address[0]))
                data = str(data).replace("'", "")
                data = data.replace("b", "")
                data = data.strip()
                print(data)
                self.gpio_action(data)
            except socket.timeout:
                break
        print("Client disconnected: {}".format(self.client_address[0]))

    def gpio_action(self, data):
        pinlist = [3, 5, 7, 8, 10]
        actionlist = data.split()
        pin = actionlist[0]
        action = actionlist[1]
        if len(actionlist)>2:
            setvalue = actionlist[2]
        
        #gpio action
        
        #setvoltage
        if action == 'SETVOLTAGE':
            if GPIO.gpio_function(int(pin)) == 0:
                if setvalue == 'True':
                    GPIO.output(int(pin), GPIO.HIGH)
                elif setvalue == 'False':
                    GPIO.output(int(pin), GPIO.LOW)
            elif GPIO.gpio_function(int(pin)) == 1:
                if setvalue == 'True':
                    GPIO.setup(int(pin), GPIO.IN,
                                pull_up_down=GPIO.PUD_UP)
                elif setvalue == 'False':
                    GPIO.setup(int(pin), GPIO.IN,
                                pull_up_down=GPIO.PUD_DOWN)
        
        #setoutput
        elif action == 'SETOUTPUT':
            if setvalue == 'True':
                GPIO.setup(int(pin), GPIO.OUT, 
                            initial=GPIO.LOW)
            elif setvalue == 'False':
                GPIO.setup(int(pin), GPIO.IN,
                             pull_up_down=GPIO.PUD_DOWN)
        
        #reset
        elif action == 'RESET':
            if pin == 'ALL':
                GPIO.cleanup( pinlist )
        
        #off
        elif action == 'OFF':
            for pinnumber in pinlist:
                if GPIO.gpio_function(pinnumber) == 0:
                    GPIO.setup(pinnumber, GPIO.OUT, initial=GPIO.LOW)
                elif GPIO.gpio_function(pinnumber) == 1:
                    GPIO.setup(pinnumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        #readvoltage
        elif action == 'READVOLTAGE':
            try:
                if GPIO.input(int(pin)) == 1:
                    boolstr = 'True'
                elif GPIO.input(int(pin)) == 0:
                    boolstr = 'False'
                self.request.sendall((boolstr).encode())
            except RuntimeError:
                boolstr = 'None'
                self.request.sendall((boolstr).encode())
        
        #readoutput
        elif action == 'READOUTPUT':
            if GPIO.gpio_function(int(pin)) == 0:
                boolstr = 'True'
            elif GPIO.gpio_function(int(pin)) == 1:
                boolstr = 'False'
            self.request.sendall((boolstr).encode())
        
        #camera (not implemented yet)
        elif action == 'CAMERA':
            if setvalue == 'ON':
                pass
            elif setvalue == 'OFF':
                pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9788
    server = socketserver.TCPServer((HOST, PORT), TCP)
    # interrupt with Ctrl+c
    server.serve_forever()
