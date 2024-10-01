"""
This module implements the REST API according to JSON IO-Link Integration
https://io-link.com/share/Downloads/IO-Link_Integration/JSON_Integration_10222_V100_Mar20.zip

References:
[1] JSON_Integration_10222_V100_Mar20.pdf from above mentioned zip-File
"""
from dataclasses import dataclass
from enum import Enum
from typing import List
import requests
import logging

from .DeviceComm import devicecomm

class StatusInfo(Enum):
    """statusInfo according to [1] Table 38"""

    DEACTIVATED = "DEACTIVATED"
    INCORRECT_DEVICE = "INCORRECT_DEVICE"
    DEVICE_STARTING = "DEVICE_STARTING"
    DEVICE_ONLINE = "DEVICE_ONLINE"
    COMMUNICATION_LOST = "COMMUNICATION_LOST"
    DIGITAL_INPUT_CQ = "DIGITAL_INPUT_C/Q"
    DIGITAL_OUTPUT_CQ = "DIGITAL_OUTPUT_C/Q"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class TransmissionRate(Enum):
    """transmissionRate according to [1] Table 38"""

    COM1 = "COM1"
    COM2 = "COM2"
    COM3 = "COM3"
    NA = "NOT_AVAILABLE"


@dataclass
class CycleTime:
    """masterCycleTime according to [1] Table 38"""
    value: float
    unit: str

@dataclass
class PortStatus:
    """Object Port Status according to [1] Table 38"""
    status_info: StatusInfo
    io_link_revision: str
    transmission_rate: TransmissionRate
    master_cycle_time: CycleTime

class Identification:
    """Read the identification of the Device. Table 54"""
    vendor_id: int
    device_id: int
    io_link_revision: str
    vendor_name: str
    vendor_text: str
    product_name: str
    product_id: str
    product_text: str
    serial_number: str
    hardware_revision: str
    firmware_revision: str
    application_specific_tag: str
    location_tag: str
    function_tag: str

class Mode(Enum):
    """mode according to [1] Table 41"""
    DEACTIVATED = "DEACTIVATED"
    IOLINK_MANUAL = "IOLINK_MANUAL"
    IOLINK_AUTOSTART = "IOLINK_AUTOSTART"
    DIGITAL_INPUT = "DIGITAL_INPUT"
    DIGITAL_OUTPUT = "DIGITAL_OUTPUT"

class ValidationAndBackup(Enum):
    """validationAndBackup according to [1] Table 41"""
    NO_DEVICE_CHECK = "NO_DEVICE_CHECK"
    TYPE_COMPATIBLE_DEVICE_V1_0 = "TYPE_COMPATIBLE_DEVICE_V1.0"
    TYPE_COMPATIBLE_DEVICE_V1_1 = "TYPE_COMPATIBLE_DEVICE_V1.1"
    TYPE_COMPATIBLE_DEVICE_V1_1_BACKUP_AND_RESTORE = "TYPE_COMPATIBLE_DEVICE_V1.1_BACKUP_AND_RESTORE"
    TYPE_COMPATIBLE_DEVICE_V1_1_RESTORE = "TYPE_COMPATIBLE_DEVICE_V1.1_RESTORE"

class IqConfiguration(Enum):
    """iqConfiguration according to [1] Table 41"""
    NOT_SUPPORTED = "NOT_SUPPORTED"
    DIGITAL_INPUT = "DIGITAL_INPUT"
    DIGITAL_OUTPUT = "DIGITAL_OUTPUT"

@dataclass
class PortConfiguration:
    """Object Port Configuration according to [1] Table 41"""
    mode: Mode
    validationAndBackup: ValidationAndBackup
    iqConfiguration: IqConfiguration
    cycleTime: CycleTime
    vendorId: int
    deviceId: int
    deviceAlias: str

@dataclass
class DeviceAlias:
    """Object DeviceAlias according to [1] Table 49"""
    deviceAlias: str
    masterNumber: int
    portNumber: int

class JsonRestApi(devicecomm):
    """
    Represents REST API according to JSON IO-Link Integration
    """

    _url_protocol = "http://"
    _url_prefix = "/iolink/v1"

    def __init__(
        self, hostname: str, master: int, port: int = None, basic_auth=None
    ) -> None:
        """
        Instantiates the REST API

            Parameters:
                hostname (str): Hostname of the machine providing the REST API
                master (int): Master number (starting with 1)
                port (int): Port number (starting with 1)
                basic auth (str, str): Username, Password. Set to None to deactivate authentication
        """
        self._hostname = hostname
        self._master = master
        self._port = port
        self._basic_auth = basic_auth

    def get_master_port_status(
        self, master: int = None, port: int = None
    ) -> PortStatus:
        """
        [1] section 5.6.3

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                port_status (PortStatus): PortStatus according to [1]
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/masters/{master}/ports/{port}/status"
        logging.debug("Request URI: " + url)
        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        port_status = PortStatus(
            status_info=StatusInfo(data["statusInfo"]),
            io_link_revision=data["iolinkRevision"],
            transmission_rate=TransmissionRate(data["transmissionRate"]),
            master_cycle_time=CycleTime(
                data["masterCycleTime"]["value"],
                data["masterCycleTime"]["unit"],
            ),
        )

        return port_status

    def get_master_port_identification(
        self, master: int = None, port: int = None
    ) -> Identification:
        """
        [1] section 5.7.3

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                port_identification (Identification): Identification according to [1]
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/master{master}port{port}/identification"
        logging.debug("Request URI: " + url)
        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        port_identification = Identification(
                vendor_id=Identification(data["vendorId"]),
                device_id=Identification(data["deviceId"]),
                io_link_revision=Identification(data["iolinkRevision"]),
                vendor_name=Identification(data["vendorName"]),
                vendor_text=Identification(data["vendorText"]),
                product_name=Identification(data["productName"]),
                product_id=Identification(data["productId"]),
                product_text=Identification(data["productText"]),
                serial_number=Identification(data["serialNumber"]),
                hardware_revision=Identification(data["hardwareRevision"]),
                firmware_revision=Identification(data["firmwareRevision"]),
                application_specific_tag=Identification(data["applicationSpecificTag"]),
                location_tag=Identification(data["locationTag"]),
                function_tag=Identification(data["functionTag"]),
        )

        return port_identification

    def get_processdata_value(
        self, master: int = None, port: int = None
    ) -> any:
        """
        [1] section 5.7.5

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                response: JSON encoded respone
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/processdata/value"
        logging.debug("Request URI: " + url)

        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        return data

    def post_processdata_value(
        self,
        iq_value: bool = None,
        cq_value: bool = None,
        io_link_value: List[int] = None,
        io_link_valid: bool = True,
        master: int = None,
        port: int = None,
    ) -> None:
        """
        [1] section 5.7.8

            Parameters:
                cq_value (bool): Activate/ deactivate CQ-Pin (if CQ-Pin is parameterized correctly)
                iq_value (bool): Activate/ deactivate IQ-Pin (if CQ-Pin is parameterized correctly)
                io_link_value (List[int]): Output data for IO-Link (io_link_value and io_link_valid can only be set together)
                io_link_valid (bool): Valid-state for io_link_value (io_link_value and io_link_valid can only be set together)
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/processdata/value"
        logging.debug("Request URI: " + url)

        json_content = {}
        if iq_value is not None:
            json_content["iqValue"] = iq_value

        if cq_value is not None:
            json_content["cqValue"] = cq_value

        if io_link_value is not None:
            json_content["iolink"] = {
                "valid": io_link_valid,
                "value": io_link_value,
            }

        logging.debug("Request data: " + str(json_content))

        response = requests.post(url, json=json_content, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

    def get_processdata_getdata_value(
        self, master: int = None, port: int = None
    ) -> any:
        """
        [1] section 5.7.5, but returns only the getData part

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                response: JSON encoded respone
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/processdata/getdata/value?format=byteArray"
        logging.debug("Request URI: " + url)

        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()

        logging.debug("Response data: " + str(data))

        return data
    
    def get_processdata_setdata_value(
        self, master: int = None, port: int = None
    ) -> any:
        """
        [1] section 5.7.5, but returns only the getData part

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                response: JSON encoded respone
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/processdata/setdata/value?format=byteArray"
        logging.debug("Request URI: " + url)

        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()

        logging.debug("Response data: " + str(data))

        return data

    def get_port_configuration(
            self,
            master: int = None,
            port: int = None
        ) -> PortConfiguration:
        """
        [1] section 5.6.4

            Parameters:
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.

            Returns:
                PortConfiguration: current configuration of the IO-Link port
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/masters/{master}/ports/{port}/configuration"
        logging.debug("Request URI: " + url)
        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        try:
            mode = Mode(data["mode"])
        except KeyError:
            mode = None
        
        try:
            validation_and_backup = ValidationAndBackup(data["validationAndBackup"])
        except KeyError:
            validation_and_backup = None

        try:
            iq_configuration = IqConfiguration(data["iqConfiguration"])
        except KeyError:
            iq_configuration = None

        try:
            cycle_time = CycleTime(int(data["cycleTime"]["value"]), data["cycleTime"]["unit"])
        except KeyError:
            cycle_time = None

        try:
            vendor_id = data["vendorId"]
        except KeyError:
            vendor_id = None

        try:
            device_id = data["deviceId"]
        except KeyError:
            device_id = None

        try:
            device_alias = data["deviceAlias"]
        except KeyError:
            device_alias = None

        port_config = PortConfiguration(
            mode=mode,
            validationAndBackup=validation_and_backup,
            iqConfiguration=iq_configuration,
            cycleTime=cycle_time,
            vendorId=vendor_id,
            deviceId=device_id,
            deviceAlias=device_alias
        )
        
        return port_config

    def post_port_configuration(
            self,
            mode: Mode = None,
            validation_and_backup: ValidationAndBackup = None,
            iq_configuration: IqConfiguration = None,
            cycle_time: CycleTime = None,
            vendor_id: int = None,
            device_id: int = None,
            device_alias: str = None,
            master: int = None,
            port: int = None
        ) -> None:
        """
        [1] section 5.6.5

            Parameters:
                mode: mode, not set in JSON request if not set.
                validation_and_backup: validationAndBackup, not set in JSON request if not set.
                iq_configuration: iqConfiguration, not set in JSON request if not set.
                cycle_time: cycleTime, not set in JSON request if not set.
                vendor_id: vendorId, not set in JSON request if not set.
                device_id: deviceId, not set in JSON request if not set.
                device_alias: deviceAlias, not set in JSON request if not set.
                master (int): Master number, taken from constructor if not set.
                port (int): Port number, taken from constructor if not set.
        """
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/masters/{master}/ports/{port}/configuration"
        logging.debug("Request URI: " + url)

        json_content = {}
        if mode is not None:
            json_content["mode"] = mode.value

        if validation_and_backup is not None:
            json_content["validationAndBackup"] = validation_and_backup.value

        if iq_configuration is not None:
            json_content["iqConfiguration"] = iq_configuration.value

        if cycle_time is not None:
            json_content["cycleTime"] = {"value": cycle_time.value, "unit": cycle_time.unit},

        if vendor_id is not None:
            json_content["vendorId"] = vendor_id

        if device_id is not None:
            json_content["deviceId"] = device_id

        if device_alias is not None:
            json_content["deviceAlias"] = device_alias

        logging.debug("Request data: " + str(json_content))

        response = requests.post(url, json=json_content, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

    def get_devices(self) -> list[DeviceAlias]:
        """
        [1] section 5.7.1

            Parameters:

            Returns:
                device_alias (Array of Element DeviceAlias): Array of Element DeviceAlias according to [1]
        """
        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices"
        logging.debug("Request URI: " + url)
        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        result = []
        for element in data:
            result.append(DeviceAlias(element["deviceAlias"], element["masterNumber"], element["portNumber"]))
        
        return result
    
    def helper_get_device_alias(self, master: int = None, port: int = None):
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        devices = self.get_devices()

        for device in devices:
            if device.portNumber == port and device.masterNumber == master:
                return device.deviceAlias
        return None
    
    def get_parameters(self, index: int, subindex: int = None, master: int = None, port: int = None) -> list[int]:
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        if subindex is None:
            url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/parameters/{index}/value?format=byteArray"
        else:
            url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/parameters/{index}/subindices/{subindex}/value?format=byteArray"
        logging.debug("Request URI: " + url)

        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        return response.json()['value']
    
    def post_parameters(self, data : list[int], index: int, subindex: int = None, master: int = None, port: int = None) -> None:
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        deviceAlias = self.helper_get_device_alias(master, port)
        if subindex is None:
            url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/parameters/{index}/value?format=byteArray"
        else:
            url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/devices/{deviceAlias}/parameters/{index}/subindices/{subindex}/value?format=byteArray"
        logging.debug("Request URI: " + url)

        respone = requests.post(url, auth=self._basic_auth, json={"value" : data})

    def get_datastorage(self, master: int = None, port: int = None) -> dict:
        if master is None:
            master = self._master
        if port is None:
            port = self._port

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/masters/{master}/ports/{port}/datastorage"

        response = requests.get(url, auth=self._basic_auth)
        response.raise_for_status()

        return response.json()
    


    def get_event(self, master: int = None, port: int = None) -> any:

        if master is None:
            master = self._master
        if port is None:
            port = self._port
    
        # GET /iolink/v1/gateway/events
        #?origin=PORTS&top=3&masterNumber=2&portNumber=7

        deviceAlias = self.helper_get_device_alias(master, port)

        url = f"{self._url_protocol}{self._hostname}{self._url_prefix}/gateway/events?bottom=1&masterNumber={master}&portNumber={port}"
        #GET /iolink/v1/gateway/events?origin=PORTS&top=1&masterNumber=2&portNumber=7&orderBy=timestamp desc
    

        logging.debug("Request URI: " + url)

        response = requests.get(url, auth=self._basic_auth)
        # handle HTTP errors as exceptions
        response.raise_for_status()

        data = response.json()
        logging.debug("Response data: " + str(data))

        return data