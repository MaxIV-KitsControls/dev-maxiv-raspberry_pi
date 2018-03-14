#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raspberry Pi GPIO-control tango device server.
Sundberg, KITS @ MAXIV 2018-03-06
"""


import time
import numpy
import socket

from tango import (Attr, AttReqType, AttrQuality, AttrWriteType, DispLevel, DevState,
                    DebugIt)
from tango.server import (Device, attribute, command, pipe,
                    device_property)

from RPi import Raspberry

class RaspberryPiIO(Device):

    #attributes
    pin3_voltage = attribute(label="PIN_3 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_3 voltage",
                        fget="get_pin3_voltage",
                        fset="set_pin3_voltage",
                        fisallowed="is_voltage_allowed")

    pin3_output = attribute(label="PIN_3 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_3 output",
                        fget="get_pin3_output",
                        fset="set_pin3_output",
                        fisallowed="is_output_allowed")

    pin5_voltage = attribute(label="PIN_5 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_5 voltage",
                        fget="get_pin5_voltage",
                        fset="set_pin5_voltage",
                        fisallowed="is_voltage_allowed")

    pin5_output = attribute(label="PIN_5 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_5 output",
                        fget="get_pin5_output",
                        fset="set_pin5_output",
                        fisallowed="is_output_allowed")

    pin7_voltage = attribute(label="PIN_7 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_7 voltage",
                        fget="get_pin7_voltage",
                        fset="set_pin7_voltage",
                        fisallowed="is_voltage_allowed")

    pin7_output = attribute(label="PIN_7 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_7 output",
                        fget="get_pin7_output",
                        fset="set_pin7_output",
                        fisallowed="is_output_allowed")

    pin8_voltage = attribute(label="PIN_8 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_8 voltage",
                        fget="get_pin8_voltage",
                        fset="set_pin8_voltage",
                        fisallowed="is_voltage_allowed")

    pin8_output = attribute(label="PIN_8 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_8 output",
                        fget="get_pin8_output",
                        fset="set_pin8_output",
                        fisallowed="is_output_allowed")

    pin10_voltage = attribute(label="PIN_10 voltage", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_10 voltage",
                        fget="get_pin10_voltage",
                        fset="set_pin10_voltage",
                        fisallowed="is_voltage_allowed")

    pin10_output = attribute(label="PIN_10 output", dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        doc="PIN_10 output",
                        fget="get_pin10_output",
                        fset="set_pin10_output",
                        fisallowed="is_output_allowed")


    info = pipe(label='Info')

    host = device_property(dtype=str)
    port = device_property(dtype=int, default_value=9788)

    #READ and WRITE states currently have the same condition
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
    def get_pin3_voltage(self):
        try:
            self.__pin3_voltage = self.raspberry.readvoltage(3)
            return self.__pin3_voltage
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin3_voltage(self, value):
        try:
            self.raspberry.setvoltage(3, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def get_pin3_output(self):
        try:
            self.__pin3_output = self.raspberry.readoutput(3)
            return self.__pin3_output
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin3_output(self, value):
        try:
            self.raspberry.setoutput(3, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    #gpio5
    def get_pin5_voltage(self):
        try:
            self.__pin5_voltage = self.raspberry.readvoltage(5)
            return self.__pin5_voltage
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin5_voltage(self, value):
        try:
            self.raspberry.setvoltage(5, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def get_pin5_output(self):
        try:
            self.__pin5_output = self.raspberry.readoutput(5)
            return self.__pin5_output
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin5_output(self, value):
        try:
            self.raspberry.setoutput(5, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    #gpio7
    def get_pin7_voltage(self):
        try:
            self.__pin7_voltage = self.raspberry.readvoltage(7)
            return self.__pin7_voltage
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin7_voltage(self, value):
        try:
            self.raspberry.setvoltage(7, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def get_pin7_output(self):
        try:
            self.__pin7_output = self.raspberry.readoutput(7)
            return self.__pin7_output
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin7_output(self, value):
        try:
            self.__pin7_output = value
            self.raspberry.setoutput(7, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    #gpio8
    def get_pin8_voltage(self):
        try:
            self.__pin8_voltage = self.raspberry.readvoltage(8)
            return self.__pin8_voltage
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin8_voltage(self, value):
        try:
            self.raspberry.setvoltage(8, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def get_pin8_output(self):
        try:
            self.__pin8_output = self.raspberry.readoutput(8)
            return self.__pin8_output
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin8_output(self, value):
        try:
            self.raspberry.setoutput(8, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)


    #gpio10
    def get_pin10_voltage(self):
        try:
            self.__pin10_voltage = self.raspberry.readvoltage(10)
            return self.__pin10_voltage
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin10_voltage(self, value):
        try:
            self.raspberry.setvoltage(10, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def get_pin10_output(self):
        try:
            self.__pin10_output = self.raspberry.readoutput(10)
            return self.__pin10_output
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)

    def set_pin10_output(self, value):
        try:
            self.raspberry.setoutput(10, value)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)
#end_of_gpio's

    def read_info(self):
        return 'Information', dict(manufacturer='Raspberry',
                                   model='Pi 3',
                                   version_number=3)

#    @DebugIt()
#    def xxx(self):


    def is_TurnOn_allowed(self):
        return self.get_state() == DevState.OFF

    @command
    def TurnOn(self):
#        if self.get_state() != DevState.OFF:
#            self.debug_stream('Device must be in OFF state to ' +
#                                'turn on.')
#            return
        self.set_state(DevState.ON)

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

if __name__ == "__main__":
    RaspberryPiIO.run_server()
