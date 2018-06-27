"""
TCP Server for the RPi GPIO tango device server.
2018-06-13.
"""

import socket
import socketserver
import RPi.GPIO as GPIO
import argparse
import subprocess

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class TCP(socketserver.BaseRequestHandler):
        
    pinlist = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16]

    def handle(self):
        #self.request.settimeout(5)
        print("Client connection: {}".format(self.client_address[0]))
        while True:
                data = self.request.recv(1024).strip()
                if not data:
                    break
                #print("{} wrote:".format(self.client_address[0]))
                data = str(data).replace("'", "")
                data = data.replace("b", "")
                data = data.strip()
                #print(data)
                self.gpio_action(data)
        print("Client disconnected: {}".format(self.client_address[0]))

    def set_voltage(self, pin, setvalue):
        if GPIO.gpio_function(int(pin)) == 1:
            boolstr = 'False'
            self.request.sendall((boolstr).encode()) 
        else:
            if setvalue == 'True':
                try:
                    GPIO.output(int(pin), GPIO.HIGH)
                except RuntimeError:
                    set_output(int(pin), 'True')
                    GPIO.output(int(pin), GPIO.HIGH)
            else:
                try:
                    GPIO.output(int(pin), GPIO.LOW)
                except RuntimeError:            
                    set_output(int(pin), 'True')
                    GPIO.output(int(pin), GPIO.LOW)
            boolstr = 'True'
            self.request.sendall((boolstr).encode())

    def set_output(self, pin, setvalue):
        if setvalue == 'True':
            GPIO.setup(int(pin), GPIO.OUT)
        else:
            GPIO.setup(int(pin), GPIO.IN)

    def reset(self, pin):
         if pin == 'ALL':
            GPIO.cleanup(self.pinlist)

    def off(self):
        for pin in self.pinlist:
            if GPIO.gpio_function(pin) == 0:
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            else:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_voltage(self, pin):
        try:
            if GPIO.input(int(pin)) == 1:
                boolstr = 'True'
            else:
                boolstr = 'False'
            self.request.sendall((boolstr).encode())
        except RuntimeError:
            boolstr = 'None'
            self.request.sendall((boolstr).encode())

    def read_output(self, pin):
        if GPIO.gpio_function(int(pin)) == 0:
            boolstr = 'True'
        else:
            boolstr = 'False'
        self.request.sendall((boolstr).encode())

    def gpio_action(self, data):
        actionlist = data.split()
        pin = actionlist[0]
        action = actionlist[1]
        if len(actionlist)>2:
            setvalue = actionlist[2]
       
        #setvoltage
        if action == 'SETVOLTAGE':
            self.set_voltage(pin, setvalue)
       
        #setoutput
        elif action == 'SETOUTPUT':
            self.set_output(pin, setvalue)

        #reset
        elif action == 'RESET':
            self.reset(pin)
       
        #off
        elif action == 'OFF':
            self.off()
       
        #readvoltage
        elif action == 'READVOLTAGE':
            self.read_voltage(pin)
       
        #readoutput
        elif action == 'READOUTPUT':
            self.read_output(pin)

def main():
    parser = argparse.ArgumentParser(description='Raspberry PI TCP/IP Server.')
    parser.add_argument('-host', metavar='HOST', type=str,
            default='0.0.0.0', help='host ip number (str)')
    parser.add_argument('-port', metavar='PORT', type=int,
            default=9788, help='host port number (int)')
    args = parser.parse_args()
    HOST, PORT = args.host, args.port
    p = subprocess.Popen("python -c 'import advanced_streamer; advanced_streamer.main()'", shell=True)
    server = socketserver.TCPServer((HOST, PORT), TCP)
    # interrupt with Ctrl+c
    server.serve_forever()

if __name__ == '__main__':
    main()
