#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raspberry Pi GPIO-control Tango device server.
2018-04-03.
"""
 

import time
import numpy
import socket

from raspberry_pi.resource import catch_connection_error

from tango import (Attr, AttReqType, AttrQuality, AttrWriteType, DispLevel,
			DevState, DebugIt)
from tango.server import (Device, attribute, command, pipe, device_property)

from raspberry_pi.RPi import Raspberry


class RaspberryPiIO(Device):

    #attributes
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
                        
    info = pipe(label='Info')

    host = device_property(dtype=str)
    port = device_property(dtype=int, default_value=9788)

    #Read and write states currently have the same condition
    def is_voltage_allowed(self, request):
        if request == AttReqType.READ_REQ:
            return (self.get_state() == DevState.ON)
        if request == AttReqType.WRITE_REQ:
            return (self.get_state() == DevState.ON)

    def is_output_allowed(self, request):
        return self.get_state() == DevState.ON
    
    def init_device(self):
        Device.init_device(self)
        self.raspberry = Raspberry(self.host)
        
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
            self.set_state(DevState.ON)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)
            self.debug_stream('Unable to connect to Raspberry Pi TCP/IP'
                                + ' server.')

    def delete_device(self):
        self.raspberry.disconnect_from_pi()
        self.raspberry = None

    #gpio3
    @catch_connection_error
    def get_pin3_voltage(self):
        self.__pin3_voltage = self.raspberry.readvoltage(3)
        return self.__pin3_voltage

    @catch_connection_error
    def set_pin3_voltage(self, value):
        self.raspberry.setvoltage(3, value)
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
        self.raspberry.setvoltage(5, value)
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
        self.raspberry.setvoltage(7, value)
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
        self.raspberry.setvoltage(8, value)
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
        self.raspberry.setvoltage(10, value)
        self.push_change_event('pin10_voltage', 
            self.get_pin10_voltage())

    @catch_connection_error
    def get_pin10_output(self):
        self.__pin10_output = self.raspberry.readoutput(10)
        return self.__pin10_output

    @catch_connection_error
    def set_pin10_output(self, value):
        self.raspberry.setoutput(10, value)
        self.push_change_event('pin10_output', self.get_pin10_output())

#End of gpio's

    def read_info(self):
        return 'Information', dict(manufacturer='Raspberry',
                                   model='Pi 3',
                                   version_number=3)

#    @DebugIt()
#    def xxx(self):

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
        
    @command
    def Camera_On(self):
        self.raspberry.camera_on()
    
    @command    
    def Camera_Off(self):
        self.raspberry.camera_off()
        
run = RaspberryPiIO.run_server()

if __name__ == "__main__":
    RaspberryPiIO.run_server()
