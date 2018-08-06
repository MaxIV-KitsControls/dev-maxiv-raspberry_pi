import pytest
import random
from collections import deque, MutableMapping
from raspberry_pi import RaspberryPiIO, RPi
from tango.test_context import DeviceTestContext
from tango import DevState, DevFailed


# Missing test
#  - Attributes:
#    - read/write ouput allowed
#    - read/write voltage allowed
#    - read image
#  - Connection fail
#  - Connection error decorator
#  - Commands
#    - TurnOn
#    - TurnOn allowed
#    - TurnOff
#    - TurnOff allowed
#    - ResetAll
#    - ResetAll allowed

class QuerryMap(MutableMapping):
    """ Dictionnary used to pre-set answers (key=request, value=reply)
        Return True if no entry has been set
        Also count the number of request
    """
    def __init__(self, *args, **kwargs):
        self._store = dict()
        self._counter = dict()
        self.history = []
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        """ Return corresponding value for one key
            Return True if no entry
            Increment the request counter
        """
        # Add request to history
        self.history.append(key)
        try:
            # Add one to the request counter
            self._counter[key] = self._counter[key] + 1
        except KeyError:
            # No value for the key, let's create it and Add one to the counter
            self[key] = True
            self._counter[key] = self._counter[key] + 1
        return self._store[key]

    def __setitem__(self, key, value):
        # Set item in both dict
        self._store[key] = value
        self._counter[key] = 0

    def __delitem__(self, key):
        # Remove item from internal dict
        del self._counter[key]
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return self._store.__repr__()


def mock_socket(mocker):
    # Create mock
    tcp = mocker.Mock()
    tcp.return_value = tcp
    # Return the same mock object when instanciate one socket
    tcp.socket.return_value = tcp
    # Setup a mapping between requests and replies
    query_map = QuerryMap()
    # Use a queue to keep request requests in order
    query_queue = deque()
    # socket.endall calls add args to the query queue
    sendall = mocker.Mock(side_effect=lambda x: query_queue.append(x))
    # socket.recv returns associted replie from the first element in the queue
    recv = mocker.Mock(side_effect=lambda x: query_map[query_queue.popleft()])
    # Setup mocks
    tcp.sendall = sendall
    tcp.recv = recv
    RPi.socket = tcp
    # Return mock and map object
    return tcp, query_map, query_queue


@pytest.yield_fixture
def scope_device(mocker):
    tcp, query_map, query_queue = mock_socket(mocker)
    with DeviceTestContext(RaspberryPiIO.RaspberryPiIO,
                           properties={"Host": "hello"}) as ds:
        yield ds, tcp, query_map, query_queue


@pytest.fixture(params=[3, 5, 7, 8, 10, 11, 12, 13, 15, 16])
def raspberry_pin(request):
    return request.param


def test_run_server(scope_device):
    ds, tcp, _, _ = scope_device
    # Assert socket is connected
    tcp.connect.assert_called_once_with(("hello", 9788))
    # Assert tango device is running
    assert ds.state() == DevState.ON


def test_pin_output(scope_device, raspberry_pin):
    attribute_name = "pin{}_output".format(raspberry_pin)
    # Extract mocks
    ds, tcp, query_map, query_queue = scope_device
    # Expected queries
    read_query = "{} READOUTPUT".format(raspberry_pin).encode()
    write_query = "{} SETOUTPUT True".format(raspberry_pin).encode()
    # Generate output
    expected_ouput = bool(random.getrandbits(1))
    # Setup socket mock answer
    query_map[read_query] = expected_ouput
    # Read tango attribute
    output = ds.read_attribute(attribute_name).value
    # Assert only one query
    assert len(query_map.history) == 1
    # Assert query
    assert read_query in query_map.history
    # Assert read out
    assert output == expected_ouput
    # Write pin output
    ds.write_attribute(attribute_name, True)
    # Assert query has been sent
    assert write_query == query_queue.popleft()


def test_pin_voltage(scope_device, raspberry_pin):
    attribute_name = "pin{}_voltage".format(raspberry_pin)
    # Extract mocks
    ds, tcp, query_map, query_queue = scope_device
    # Expected query
    read_query = "{} READVOLTAGE".format(raspberry_pin).encode()
    # Generate output
    expected_output = bool(random.getrandbits(1))
    # Setup socket mock answer
    query_map[read_query] = expected_output
    # Read tango attribute
    output = ds.read_attribute(attribute_name).value
    # Assert only one query
    assert len(query_map.history) == 1
    # Assert query
    assert read_query in query_map.history
    # Assert read out
    assert output == expected_output
    # Write query
    write_query = "{} SETVOLTAGE {}".format(raspberry_pin, expected_output)
    write_query = write_query.encode()
    # Except exception if the attribute output is not set to true
    with pytest.raises(DevFailed):
        ds.write_attribute(attribute_name, expected_output)
    assert not query_queue
    # Setup pin output to True (by default the query map object return True
    # so simply read the output tango attribute set pinout to true
    ds.read_attribute("pin{}_output".format(raspberry_pin))
    ds.write_attribute(attribute_name, expected_output)
    assert write_query in query_map.history
