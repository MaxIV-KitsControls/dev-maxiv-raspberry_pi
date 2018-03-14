"""
TCP Server for the tango-device RPi GPIO
Sundberg, KITS @ MAXIV, 2018-03-06
"""

import socketserver
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class TCP(socketserver.BaseRequestHandler):
    

    def handle(self):
        print("Client connection: {}".format(self.client_address[0]))
        while True:
            data = self.request.recv(1024).strip()
            if not data:
                break
            print("{} wrote:".format(self.client_address[0]))
            data = str(data).replace("'", "")
            data = data.replace("b", "")
            data = data.strip()
            print(data)
            self.gpio_action(data)
        print("Client disconnected: {}".format(self.client_address[0]))

    def gpio_action(self, data):
        pinlist = [3, 5, 7, 8, 10]
        actionlist = data.split()
        
        #gpio action
        if len(actionlist) < 2:
            print('fail')
            return
        if actionlist[1] == 'SETVOLTAGE':
            if GPIO.gpio_function(int(actionlist[0])) == 0:
                if actionlist[2] == 'True':
                    GPIO.output(int(actionlist[0]), GPIO.HIGH)
                elif actionlist[2] == 'False':
                    GPIO.output(int(actionlist[0]), GPIO.LOW)
            elif GPIO.gpio_function(int(actionlist[0])) == 1:
                if actionlist[2] == 'True':
                    GPIO.setup(int(actionlist[0]), GPIO.IN,
                                pull_up_down=GPIO.PUD_UP)
                elif actionlist[2] == 'False':
                    GPIO.setup(int(actionlist[0]), GPIO.IN,
                                pull_up_down=GPIO.PUD_DOWN)
                            
        elif actionlist[1] == 'SETOUTPUT':
            if actionlist[2] == 'True':
                GPIO.setup(int(actionlist[0]), GPIO.OUT, 
                            initial=GPIO.LOW)
            elif actionlist[2] == 'False':
                GPIO.setup(int(actionlist[0]), GPIO.IN,
                             pull_up_down=GPIO.PUD_DOWN)
                            
        elif actionlist[1] == 'RESETALL':
            GPIO.cleanup( pinlist )
            
        elif actionlist[1] == 'OFF':
            for pin in pinlist:
                if GPIO.gpio_function(pin) == 0:
                    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                elif GPIO.gpio_function(pin) == 1:
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                
        elif actionlist[1] == 'READVOLTAGE':
            try:
                mode = GPIO.input(int(actionlist[0]))
                if mode == 1:
                    boolstr = 'True'
                elif mode == 0:
                    boolstr = 'False'
                self.request.sendall((boolstr).encode())
            except:
                boolstr = 'None'
                self.request.sendall((boolstr).encode())
                
        elif actionlist[1] == 'READOUTPUT':
            mode = GPIO.gpio_function(int(actionlist[0]))
            if mode == 0:
                boolstr = 'True'
            elif mode == 1:
                boolstr = 'False'
            self.request.sendall((boolstr).encode())

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9788
    server = socketserver.TCPServer((HOST, PORT), TCP)
    # interrupt with Ctrl+c
    server.serve_forever()
