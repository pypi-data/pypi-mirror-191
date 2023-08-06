"""Class handle base info about device."""
from collections import defaultdict
import logging
import json

from typing import Any, Callable

from inelsmqtt.util import DeviceValue
from inelsmqtt import InelsMqtt
from inelsmqtt.const import (
    DEVICE_TYPE_DICT,
    FRAGMENT_DOMAIN,
    INELS_DEVICE_TYPE_DICT,
    MANUFACTURER,
    SENSOR,
    BUTTON,
    TOPIC_FRAGMENTS,
    FRAGMENT_DEVICE_TYPE,
    FRAGMENT_SERIAL_NUMBER,
    FRAGMENT_UNIQUE_ID,
    DEVICE_CONNECTED,
    VERSION,
    INELS_DEVICE_TYPE_TO_KEY_INDEX
)

_LOGGER = logging.getLogger(__name__)


class Device(object):
    """Carry basic device stuff

    Args:
        object (_type_): default object it is new style of python class coding
    """

    def __init__(
        self,
        mqtt: InelsMqtt,
        state_topic: str,
        title: str = None,
    ) -> None:
        """Initialize instance of device

        Args:
            mqtt (InelsMqtt): instance of mqtt broker
            status_topic (str): String format of status topic
            set_topic (str): Sring format of set topic
            title (str, optional): Formal name of the device. When None
            then will be same as unique_id. Defaults to None.
        """
        fragments = state_topic.split("/")

        self.__mqtt = mqtt
        self.__device_type = DEVICE_TYPE_DICT[
            fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        ]
        self.__inels_type = INELS_DEVICE_TYPE_DICT[
            fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        ]
        self.__unique_id = fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]
        self.__parent_id = fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]
        self.__state_topic = state_topic
        self.__set_topic = None

        if self.__device_type is not SENSOR and self.__device_type is not BUTTON:
            self.__set_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/set/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # noqa: E501

        self.__connected_topic = f"{fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]}/connected/{fragments[TOPIC_FRAGMENTS[FRAGMENT_SERIAL_NUMBER]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]}/{fragments[TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]]}"  # noqa: E501
        self.__title = title if title is not None else self.__unique_id
        self.__domain = fragments[TOPIC_FRAGMENTS[FRAGMENT_DOMAIN]]
        self.__state: Any = None
        self.__values: DeviceValue = None
        self.__last_values: DeviceValue = None
    

        self.__key_index_to_byte: dict[tuple[str, int], int] = INELS_DEVICE_TYPE_TO_KEY_INDEX.get(self.__inels_type)
        self.__callback_map: dict[int, list[Callable[[Any], Any]]] = defaultdict(lambda: list())
        # subscribe availability
        self.__mqtt.subscribe(self.__connected_topic, 0, None, None)

    @property
    def unique_id(self) -> str:
        """Get unique_id of the device

        Returns:
            str: Unique ID
        """
        return self.__unique_id

    @property
    def is_subscribed(self) -> bool:
        """Is device subscribed to mqtt

        Returns:
            bool: True/False
        """
        return self.__mqtt.is_subscribed(self.__state_topic)

    @property
    def inels_type(self) -> str:
        """Get inels type of the device

        Returns:
            str: Type
        """
        return self.__inels_type

    @property
    def device_type(self) -> str:
        """Get type of the device

        Returns:
            str: Type
        """
        return self.__device_type

    @property
    def parent_id(self) -> str:
        """Get Id of the controller (PLC, Bridge)

        Returns:
            str: Parent ID
        """
        return self.__parent_id

    @property
    def title(self) -> str:
        """Get name of the device

        Returns:
            str: Name
        """
        return self.__title

    @property
    def is_available(self) -> bool:
        """Get info about availability of device

        Returns:
            bool: True/False
        """
        val = self.__mqtt.messages()[self._Device__connected_topic]
        if isinstance(val, (bytes, bytearray)):
            val = val.decode()

        return DEVICE_CONNECTED.get(val) and self.__values is not None and self.__values.__ha_value is not None

    @property
    def set_topic(self) -> str:
        """Set topic

        Returns:
            str: string of the set topic
        """
        return self.__set_topic

    @property
    def state_topic(self) -> str:
        """State topic

        Returns:
            str: string of the status topic
        """
        return self.__state_topic

    @property
    def domain(self) -> str:
        """Domain name of the topic
           it should represent the manufacturer

        Returns:
            str: Name of the domain
        """
        return self.__domain

    @property
    def state(self) -> Any:
        """State of the device."""
        if self.__state is None:
            self.get_value()

        return self.__state

    @property
    def values(self) -> DeviceValue:
        """Get values of inels and ha type."""
        return self.__values

    @property
    def last_values(self) -> DeviceValue:
        """Get last value of the device

        Returns:
            DeviceValue: latest values in many formats
        """
        return self.__last_values
        #return self.__get_value(self.__mqtt.last_value(self.__state_topic))

    @property
    def mqtt(self) -> InelsMqtt:
        """Instnace of broker."""
        return self.__mqtt

    def update_value(self, new_value: Any) -> DeviceValue:
        """Update value after broker change it."""
        _LOGGER.info("UPDATE_VALUE")
        return self.__get_value(new_value)

    def __get_value(self, val: Any) -> DeviceValue:
        """Get value and transform into the DeviceValue."""
        _LOGGER.info("__GET_VALUE")

        dev_value = DeviceValue(
            self.__device_type,
            self.__inels_type,
            inels_value=(val.decode() if val is not None else None),
        )
        self.__last_values = self.__values
        self.__state = dev_value.ha_value
        self.__values = dev_value

        return dev_value

    def get_value(self) -> DeviceValue:
        """Get value from inels

        Returns:
            Any: DeviceValue
        """
        _LOGGER.info("GET_VALUE")

        val = self.__mqtt.messages().get(self.state_topic)
        return self.__get_value(val)

    def set_ha_value(self, value: Any) -> bool:
        """Set HA value. Will automaticaly convert HA value
        into the inels value format.

        Args:
            value (Any): Object value belonging to HA device
        Returns:
            true/false if publishing is successfull or not
        """
        dev = DeviceValue(
            self.__device_type,
            self.__inels_type,
            ha_value=value,
            last_value=self.__state,
        )

        self.__state = dev.ha_value
        self.__values = dev

        ret = False
        if self.__set_topic is not None:
            ret = self.__mqtt.publish(self.__set_topic, dev.inels_set_value)

        return ret

    def info(self):
        """Device info."""
        return DeviceInfo(self)

    def info_serialized(self) -> str:
        """Device info in json format string

        Returns:
            str: JSON string format
        """
        info = {
            "name": self.__title,
            "device_type": self.__device_type,
            "id": self.__unique_id,
            "via_device": self.__parent_id,
        }

        json_serialized = json.dumps(info)
        _LOGGER.info("Device: %s", json_serialized)

        return json_serialized

    def add_callback(self, key: str, index: int, fnc: Callable[[Any], Any]) -> None:
        """Add an entity callback to the callback_map"""
        t: tuple[str, int] = (key, index)

        if self.__key_index_to_byte is not None and t not in self.__key_index_to_byte:
            byte_index = self.__key_index_to_byte[t]

            self.__callback_map[byte_index].append(fnc)
            _LOGGER.info("Added callback for %s.%d for byte %d", key, index, byte_index)
        else:
            #fallback for no key_index_to_byte_map or non-indexed entity
            self.__callback_map[-1].append(fnc)
            _LOGGER.info("Added callback for %s.%d (unknown byte)", key, index)

    

    def callback(self, new_value: Any) -> None:
        """Update value in device and call the callbacks of the respective entities."""
        _LOGGER.info("Calling update_value")
        self.update_value(new_value) #calculate status value
        
        #call all the associated values
        byte_indexes = self.diff(
            last_val=self.mqtt.last_value(self.state_topic).decode('utf-8'),
            curr_val=self.values.inels_status_value
        )

        #evaluate the callback map to see if there is a single empty callback byte without indexes

        callbacks: set[Callable[[Any], Any]] = set()

        for b in byte_indexes:
            if len(self.__callback_map[b]) == 0:
                _LOGGER.info("Calling all callbacks")
                # Call all callbacks
                for key in self.__callback_map.keys():
                    for c in self.__callback_map[key]:
                        c(new_value)

                return
            else:
                # Add it to the list of callbacks to call
                for c in self.__callback_map[b]:
                    callbacks.add(c)

        _LOGGER.info("Calling associated %d callbacks", len(callbacks))
        for c in callbacks:
            c(new_value)


    def diff(self, last_val: str, curr_val: str) -> "list[int]": 
        curr_val = curr_val.split("\n")[:-1]
        if last_val is None:
            return [i for i in range(len(curr_val))]
        last_val = last_val.split("\n")[:-1]
        l = []
        for i in range(min(len(last_val), len(curr_val))):
            if last_val[i] != curr_val[i]:
                l.append(i)
        _LOGGER.info("Found %d different bytes", len(l))

        return l

class DeviceInfo(object):
    """Device info class."""

    def __init__(self, device: Device) -> None:
        """Create object of the class

        Args:
            device (Device): device object
        """
        self.__device = device

    @property
    def manufacturer(self) -> str:
        """Manufacturer property."""
        return MANUFACTURER

    @property
    def sw_version(self) -> str:
        """Version of software."""
        return VERSION

    @property
    def model_number(self) -> str:
        """Modle of the device."""
        return self.__device.inels_type

    @property
    def serial_number(self) -> str:
        """Serial number of the device."""
        return self.__device.unique_id
