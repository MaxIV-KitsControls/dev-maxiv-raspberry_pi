#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raspberry Pi GPIO-control Tango device server.
KITS 2018-05-31.
"""
 

import socket

import numpy as np
import requests

from raspberry_pi.resource import catch_connection_error

from tango import AttReqType, AttrWriteType, DispLevel
from tango import DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

from raspberry_pi.RPi import Raspberry


class Reader():

    def __init__(self, event_source, char_enc='utf-8'):
        self._event_source = event_source
        self._char_enc = char_enc

    def _read(self):
        data = b''
        for frame in self._event_source:
            for line in frame.splitlines(True):
                data += line
                if data.endswith(b'\r\n\r\n'):
                    yield data
                    data = b''
        if data:
            yield data
        print("Done")

    def events(self):
        i = 0
        while True:
            try:
                frame = b''
                for data in self._read():
                    frame += data
                    if len(frame) >= 307200:
                        yield frame
                        #print("yield frame {}".format(i))
                        i += 1
                        frame = b''
            except Exception as e:
                print("Exception", e)
                break


class RaspberryPiIO(Device):
   
    #attributes
    image = attribute(dtype=((int,),), max_dim_x=2000, max_dim_y=2000)

    pin3_voltage = attribute(label="PIN_3 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_3 voltage",
                        fget="get_pin3_voltage",
                        fset="set_pin3_voltage",
                        fisallowed="is_voltage_allowed",
                        polling_period=1000)

    pin3_output = attribute(label="PIN_3 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_3 output",
                        fget="get_pin3_output",
                        fset="set_pin3_output",
                        fisallowed="is_output_allowed",
                        polling_period=1000)

    pin5_voltage = attribute(label="PIN_5 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_5 voltage",
                        fget="get_pin5_voltage",
                        fset="set_pin5_voltage",
                        fisallowed="is_voltage_allowed",
                        polling_period=1000)

    pin5_output = attribute(label="PIN_5 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_5 output",
                        fget="get_pin5_output",
                        fset="set_pin5_output",
                        fisallowed="is_output_allowed",
                        polling_period=1000)

    pin7_voltage = attribute(label="PIN_7 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_7 voltage",
                        fget="get_pin7_voltage",
                        fset="set_pin7_voltage",
                        fisallowed="is_voltage_allowed",
                        polling_period=1000)

    pin7_output = attribute(label="PIN_7 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_7 output",
                        fget="get_pin7_output",
                        fset="set_pin7_output",
                        fisallowed="is_output_allowed",
                        polling_period=1000)

    pin8_voltage = attribute(label="PIN_8 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_8 voltage",
                        fget="get_pin8_voltage",
                        fset="set_pin8_voltage",
                        fisallowed="is_voltage_allowed",
                        polling_period=1000)

    pin8_output = attribute(label="PIN_8 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_8 output",
                        fget="get_pin8_output",
                        fset="set_pin8_output",
                        fisallowed="is_output_allowed",
                        polling_period=1000)

    pin10_voltage = attribute(label="PIN_10 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_10 voltage",
                        fget="get_pin10_voltage",
                        fset="set_pin10_voltage",
                        fisallowed="is_voltage_allowed",
                        polling_period=1000)

    pin10_output = attribute(label="PIN_10 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_10 output",
                        fget="get_pin10_output",
                        fset="set_pin10_output",
                        fisallowed="is_output_allowed",
                        polling_period=1000)

    Host = device_property(dtype=str)
    Port = device_property(dtype=int, default_value=9788)

    def init_device(self):
        Device.init_device(self)
        self.raspberry = Raspberry(self.Host)
 
        #Event flags
        self.set_change_event('pin3_voltage', True, True)
        self.set_change_event('pin5_voltage', True, True)
        self.set_change_event('pin7_voltage', True, True)
        self.set_change_event('pin8_voltage', True, True)
        self.set_change_event('pin10_voltage', True, True)
        self.set_change_event('pin3_output', True, True)
        self.set_change_event('pin5_output', True, True)
        self.set_change_event('pin7_output', True, True)
        self.set_change_event('pin8_output', True, True)
        self.set_change_event('pin10_output', True, True)
        
        #No error decorator for the init function
        try:
            self.raspberry.connect_to_pi()
            url = 'http://' + self.Host + ':5000/stream'        
            response = requests.get(url, stream=True)
            
            self.reader = Reader(response)
            self.frame = self.get_frame()
            self.set_state(DevState.ON)
     
        except (BrokenPipeError, ConnectionRefusedError,
                ConnectionError, socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)
            self.debug_stream('Unable to connect to Raspberry Pi TCP/IP'
                                + ' server.')

    def get_frame(self):
        for event in self.reader.events():
            try:
                event = event.strip(b'\r\n\r\n')
                decoded = np.asarray(bytearray(event), dtype=np.uint8)
                decoded = decoded.reshape(480, 640)
                yield decoded
            except Exception as e:
                print("Missing frame")
                print(e)

    def read_image(self):
        l = next(self.frame)
        return l

    def delete_device(self):
        self.raspberry.disconnect_from_pi()
        self.raspberry = None

    #Read and write states currently have the same condition
    def is_voltage_allowed(self, request):
        if request == AttReqType.READ_REQ:
            return (self.get_state() == DevState.ON)
        if request == AttReqType.WRITE_REQ:
            return (self.get_state() == DevState.ON)

    def is_output_allowed(self, request):
        return self.get_state() == DevState.ON

    def set_voltage(self, value, pin, output):
        if not output:
            raise ValueError("Pin must be setup as an output first")
            return 0
        else:
            self.raspberry.setvoltage(pin, value)
            return 1

    #gpio3
    @catch_connection_error
    def get_pin3_voltage(self):
        self.__pin3_voltage = self.raspberry.readvoltage(3)
        return self.__pin3_voltage

    @catch_connection_error
    def set_pin3_voltage(self, value):
        changed = self.set_voltage(value, 3, self.__pin3_output)
        if changed:
            self.push_change_event('pin3_voltage', self.get_pin3_voltage())

    @catch_connection_error
    def get_pin3_output(self):
        self.__pin3_output = self.raspberry.readoutput(3)
        return self.__pin3_output

    @catch_connection_error
    def set_pin3_output(self, value):
        self.raspberry.setoutput(3, value)
        self.push_change_event('pin3_output', self.get_pin3_output())

    #gpio5
    @catch_connection_error
    def get_pin5_voltage(self):
        self.__pin5_voltage = self.raspberry.readvoltage(5)
        return self.__pin5_voltage

    @catch_connection_error
    def set_pin5_voltage(self, value):
        changed = self.set_voltage(value, 5, self.__pin5_output)
        if changed:
            self.push_change_event('pin5_voltage', self.get_pin5_voltage())
            
    @catch_connection_error
    def get_pin5_output(self):
        self.__pin5_output = self.raspberry.readoutput(5)
        return self.__pin5_output
            
    @catch_connection_error
    def set_pin5_output(self, value):
        self.raspberry.setoutput(5, value)
        self.push_change_event('pin5_output', self.get_pin5_output())

    #gpio7
    @catch_connection_error
    def get_pin7_voltage(self):
        self.__pin7_voltage = self.raspberry.readvoltage(7)
        return self.__pin7_voltage

    @catch_connection_error
    def set_pin7_voltage(self, value):
       changed = self.set_voltage(value, 7, self.__pin7_output)
       if changed:
           self.push_change_event('pin7_voltage', self.get_pin7_voltage())

    @catch_connection_error
    def get_pin7_output(self):
        self.__pin7_output = self.raspberry.readoutput(7)
        return self.__pin7_output

    @catch_connection_error
    def set_pin7_output(self, value):
        self.raspberry.setoutput(7, value)
        self.push_change_event('pin7_output', self.get_pin7_output())

    #gpio8
    @catch_connection_error
    def get_pin8_voltage(self):
        self.__pin8_voltage = self.raspberry.readvoltage(8)
        return self.__pin8_voltage

    @catch_connection_error
    def set_pin8_voltage(self, value):
        changed = self.set_voltage(value, 8, self.__pin8_output)
        if changed:
            self.push_change_event('pin8_voltage', self.get_pin8_voltage())

    @catch_connection_error
    def get_pin8_output(self):
        self.__pin8_output = self.raspberry.readoutput(8)
        return self.__pin8_output

    @catch_connection_error
    def set_pin8_output(self, value):
        self.raspberry.setoutput(8, value)
        self.push_change_event('pin8_output', self.get_pin8_output())

    #gpio10
    @catch_connection_error
    def get_pin10_voltage(self):
        self.__pin10_voltage = self.raspberry.readvoltage(10)
        return self.__pin10_voltage

    @catch_connection_error
    def set_pin10_voltage(self, value):
       changed = self.set_voltage(value, 10, self.__pin10_output)
       if not changed:
           self.push_change_event('pin10_voltage', self.get_pin10_voltage())

    @catch_connection_error
    def get_pin10_output(self):
        self.__pin10_output = self.raspberry.readoutput(10)
        return self.__pin10_output

    @catch_connection_error
    def set_pin10_output(self, value):
        self.raspberry.setoutput(10, value)
        self.push_change_event('pin10_output', self.get_pin10_output())
    #End of gpio's

    def is_TurnOff_allowed(self):
        return self.get_state() == DevState.ON

    @command
    def TurnOff(self):
        self.raspberry.turnoff()
        self.set_state(DevState.OFF)

    def is_ResetAll_allowed(self):
        return self.get_state() == DevState.ON

    @command
    def ResetAll(self):
        self.raspberry.resetall()
        
run = RaspberryPiIO.run_server

if __name__ == "__main__":
    RaspberryPiIO.run_server()
