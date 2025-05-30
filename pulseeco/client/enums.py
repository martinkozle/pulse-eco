import sys

if sys.version_info < (3, 11):
    from enum import Enum

    class StrEnum(str, Enum):
        def __repr__(self) -> str:
            return str.__repr__(self.value)

else:  # pragma: no cover
    from enum import StrEnum


class SensorType(StrEnum):
    # unknown type
    TYPE_NEG_1 = "-1"
    # MOEPP measurement station
    TYPE_0 = "0"
    # SkopjePulse LoRaWAN based sensor, version 1
    TYPE_1 = "1"
    # SkopjePulse WiFi based sensor, version 1
    TYPE_2 = "2"
    # pulse.eco WiFi based sensor, version 2
    TYPE_3 = "3"
    # pulse.eco LoRaWAN based sensor. version 2
    TYPE_4 = "4"
    # TODO: check what it is
    TYPE_6 = "6"
    # pengy device, version 1
    TYPE_20001 = "20001"
    # URAD Monitor device
    TYPE_20002 = "20002"
    # AirThings platform device
    TYPE_20003 = "20003"
    # sensor.community crowdsourced device
    TYPE_20004 = "20004"
    # unknown type
    TYPE_20005 = "20005"
    # unknown type
    TYPE_20006 = "20006"


class SensorStatus(StrEnum):
    # A user requested this location with a device ID, but not sending data yet
    REQUESTED = "REQUESTED"
    # The sensor is up and running properly
    ACTIVE = "ACTIVE"
    # The sensor is up and running properly but not yet confirmed by the community lead
    ACTIVE_UNCONFIRMED = "ACTIVE_UNCONFIRMED"
    # The sensor is registered but turned off and ignored
    INACTIVE = "INACTIVE"
    # The sensor is registered, but so far not bound to an owner
    NOT_CLAIMED = "NOT_CLAIMED"
    # The sensor is registered, but so far not bound to an owner nor confirmed by the community lead
    NOT_CLAIMED_UNCONFIRMED = "NOT_CLAIMED_UNCONFIRMED"
    # The sensor is manually removed from evidence in order to keep data sanity
    BANNED = "BANNED"


class DataValueType(StrEnum):
    NO2 = "no2"
    NO2_PPB = "no2_ppb"
    O3 = "o3"
    SO2 = "so2"
    CO = "co"
    CO_PPB = "co_ppb"
    NH3 = "nh3"
    NH3_PPM = "nh3_ppm"
    NH3_PPB = "nh3_ppb"
    PM25 = "pm25"
    PM10 = "pm10"
    PM1 = "pm1"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    NOISE = "noise"
    NOISE_DBA = "noise_dba"
    GAS_RESISTANCE = "gasResistance"


class AveragePeriod(StrEnum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
