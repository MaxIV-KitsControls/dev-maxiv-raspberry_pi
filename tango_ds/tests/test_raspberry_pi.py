import pytest
from tango.test_utils import DeviceTestContext
from tango import DevFailed
import raspberry_pi.RaspberryPiIO

@pytest.fixture
def socket_mock(mocker):
    path = "raspberry_pi.RPi.socket.socket"
    mock = mocker.Mock()
    mocker.patch(path).return_value = mock
    yield mock 

@pytest.fixture
def device_proxy():
    with DeviceTestContext(RaspberryPiIO, properties={'host':'hello world!'}) as device:
        yield device, socket_mock

def test_server_running(device_proxy):
    device, mock = device_proxy
    assert device.State()

def test_test():
    assert False

'''
def test_on_state(device_proxy):
    device_proxy.command_inout("TurnOn")
    read_out = device_proxy.read_attribute("State")
    assert read_out
    assert str(read_out.value) == "ON"


def test_off_state(device_proxy):
    device_proxy.command_inout("TurnOn")
    device_proxy.command_inout("TurnOff")
    read_out = device_proxy.read_attribute("State")
    assert read_out
    assert str(read_out.value) == "OFF"


def test_wavefrom_attribute(device_proxy):
    with pytest.raises(DevFailed):
        # Expect to get an exception if the acquisition is not on
        read_out = device_proxy.read_attribute("waveform")
    device_proxy.command_inout("TurnOn")
    read_out = device_proxy.read_attribute("waveform")
    assert read_out
    assert len(read_out.value) == 200


def test_maximum_attribute(device_proxy):
    try:
        device_proxy.command_inout("TurnOn")
        device_proxy.read_attribute("waveform")
    except DevFailed:
        pytest.xfail()
    read_out = device_proxy.read_attribute("maximum")
    assert read_out
    assert read_out.value >= 0.5
'''
