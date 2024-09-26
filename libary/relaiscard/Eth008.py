from .Relaiscard import RelaisCard
import socket

class Eth800(RelaisCard):

    def __init__(self, host: str = "eth008", port: int = 17494) -> None:
        """
        Instantiates the Eth008 TCP/IP Interface

            Parameters:
                host (str): Hostname of the Eth008
                port (int): Port of the interface
        """
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def set_relais_state(self, channel: int, on: bool = True) -> None:
        """
        Sets the state of a specific relais

            Parameters:
                channel (int): 1 to 8
                on (bool): True: close relais; False open relais
        """
        if on:
            command_id = 0x20
        else:
            command_id = 0x21
        command = [command_id, channel, 0] # 0 means change is not automatically reset after specific time
        self._socket.settimeout(1.0)
        self._socket.send(bytes(command))
        response = self._socket.recv(1)
        if response != b"\0":
            raise TimeoutError("No response from ETH008 received")

if __name__ == "__main__":
    r = Eth800("192.168.1.200")
    for i in range(1, 9):
        r.set_relais_state(i, True)
