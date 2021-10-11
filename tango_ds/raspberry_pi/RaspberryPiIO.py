#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raspberry Pi GPIO-control Tango device server and http camera stream.
KITS 2018-05-31.
"""

import re
import socket

import numpy as np
import requests

from raspberry_pi.resource import catch_connection_error

from tango import (AttReqType,
                   AttrWriteType,
                   DispLevel,
                   CmdArgType,
                   Attr,
                   READ_WRITE)
from tango import DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

from raspberry_pi.RPi import Raspberry


class RaspberryPiIO(Device):
    Host = device_property(dtype=str)
    Port = device_property(dtype=int, default_value=9788)
    pins = device_property(dtype=(int,))

    def _get_pin(self, attr_name):
        m = re.search('\s*(?P<pin>[\d]+)\s*', attr_name)
        if m:
            pin_number =  m.groupdict().get('pin', None)
        else:
            pin_number = None

        if pin_number is None:
            raise Exception('Error geting pin number from  [{}]'.format(attr_name))

        return pin_number

    def initialize_dynamic_attributes(self):
        for pin_number in self.pins:
            # Create attribute name
            voltage_attrname = "pin{}_voltage".format(pin_number)
            output_attrname = "pin{}_output".format(pin_number)
            # Get tango type
            tango_type = CmdArgType.DevBoolean
            # Create attributes
            voltage_attr = Attr(voltage_attrname,
                                      tango_type, READ_WRITE)
            output_attr = Attr(output_attrname,
                                     tango_type, READ_WRITE)
            # Add attribute and setup read/write/allowed method
            self.add_attribute(
                voltage_attr,
                r_meth=self.read_pin_voltage,
                w_meth=self.write_pin_voltage,
                is_allo_meth=self.is_voltage_allowed)
            self.add_attribute(
                output_attr,
                r_meth=self.read_pin_output,
                w_meth=self.write_pin_output,
                is_allo_meth=self.is_output_allowed)
            # If event needed, setup change event
            #self.set_change_event(voltage_attrname, True, True)
            #self.set_change_event(output_attrname, True, True)

            # Voltage

    @catch_connection_error
    def read_pin_voltage(self, attr):
        attr_name = attr.get_name()
        pin_number = self._get_pin(attr_name)
        value = self.raspberry.readvoltage(pin_number)
        setattr(self, "pin{}_voltage".format(pin_number), value)
        attr.set_value(value)

    @catch_connection_error
    def write_pin_voltage(self, attr):
        w_value = attr.get_write_value()
        attr_name = attr.get_name()
        pin_number = self._get_pin(attr_name)
        python_attr = "pin{}_voltage".format(pin_number)
        self.set_voltage(w_value, pin_number, getattr(self, python_attr))
        setattr(self, "{}".format(attr_name), w_value)

    # Ouptut

    @catch_connection_error
    def read_pin_output(self, attr):
        attr_name = attr.get_name()
        pin_number = self._get_pin(attr_name)
        value = self.raspberry.readoutput(pin_number)
        setattr(self, "__pin{}_output".format(pin_number), value)
        attr.set_value(value)

    @catch_connection_error
    def write_pin_output(self, attr):
        w_value = attr.get_write_value()
        attr_name = attr.get_name()
        pin_number = self._get_pin(attr_name)
        self.raspberry.setoutput(pin_number, w_value)

    def init_device(self):
        Device.init_device(self)
        self.raspberry = Raspberry(self.Host)

        #Event flags
        #self.set_change_event('pin3_voltage', True, True)
        #self.set_change_event('pin5_voltage', True, True)
        #self.set_change_event('pin7_voltage', True, True)
        #self.set_change_event('pin8_voltage', True, True)
        #self.set_change_event('pin10_voltage', True, True)
        #self.set_change_event('pin11_voltage', True, True)
        #self.set_change_event('pin12_voltage', True, True)
        #self.set_change_event('pin13_voltage', True, True)
        #self.set_change_event('pin15_voltage', True, True)
        #self.set_change_event('pin16_voltage', True, True)
        #self.set_change_event('pin3_output', True, True)
        #self.set_change_event('pin5_output', True, True)
        #self.set_change_event('pin7_output', True, True)
        #self.set_change_event('pin8_output', True, True)
        #self.set_change_event('pin10_output', True, True)
        #self.set_change_event('pin11_output', True, True)
        #self.set_change_event('pin12_output', True, True)
        #self.set_change_event('pin13_output', True, True)
        #self.set_change_event('pin15_output', True, True)
        #self.set_change_event('pin16_output', True, True)

        #No error decorator for the init function
        try:
            self.raspberry.connect_to_pi()
            self.set_state(DevState.ON)

        except (BrokenPipeError, ConnectionRefusedError,
                ConnectionError, socket.timeout, TimeoutError) as connectionerror:
            self.set_state(DevState.FAULT)
            self.debug_stream('Unable to connect to Raspberry Pi TCP/IP'
                                + ' server.')

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
        if not output or output is None:
            raise ValueError("Pin must be setup as an output first")
        else:
            request = self.raspberry.setvoltage(pin, value)
            if not request:
                raise ValueError("Pin must be setup as an output first")

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
