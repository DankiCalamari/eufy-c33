from homeassistant.const import Platform

DOMAIN = "eufy_c33"
PLATFORMS = [Platform.LOCK]

CONF_HOST = "host"
CONF_MAC_ADDRESS = "mac_address"
CONF_LOCAL_KEY = "local_key"

DEFAULT_PORT = 55556
DEFAULT_TIMEOUT = 10

ATTR_BATTERY_LEVEL = "battery_level"
ATTR_WIFI_SIGNAL = "wifi_signal"
ATTR_LOCK_STATE = "lock_state"

LOCK_STATES = {
    0: "unlocked",
    1: "locked", 
    2: "jammed",
    3: "unknown"
}