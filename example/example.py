#!/usr/bin/python3
import argparse
from time import sleep

from pycomfoconnect import *

parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='ip address of the bridge')
args = parser.parse_args()

## Configuration #######################################################################################################

pin = 0
local_name = 'Computer'
local_uuid = bytes.fromhex('00000000000000000000000000000005')

## Bridge discovery ####################################################################################################

# Method 1: Use discovery to initialise Bridge
# bridges = Bridge.discover(timeout=1)
# if bridges:
#     bridge = bridges[0]
# else:
#     bridge = None

# Method 2: Use direct discovery to initialise Bridge
bridges = Bridge.discover(args.ip)
if bridges:
    bridge = bridges[0]
else:
    bridge = None

# Method 3: Setup bridge manually
# bridge = Bridge(args.ip, bytes.fromhex('0000000000251010800170b3d54264b4'))

if bridge is None:
    print("No bridges found!")
    exit(1)

print("Bridge found: %s (%s)" % (bridge.uuid.hex(), bridge.host))
bridge.debug = True


## Setting up a session ########################################################################################

def callback(var, value):
#    print("%s = %s" % (var, value))
    pass


# Setup a Comfoconnect session
comfoconnect = ComfoConnect(bridge, local_uuid, local_name, pin)
comfoconnect.callback = callback

try:
    # Connect to the bridge
    # comfoconnect.connect(False)  # Don't disconnect existing clients.
    comfoconnect.connect(True)  # Disconnect existing clients.

except Exception as e:
    print('ERROR: %s' % e)
    exit(1)

## Execute functions ###############################################################################################

# ListRegisteredApps
# for app in comfoconnect.cmd_list_registered_apps():
#     print('%s: %s' % (app['uuid'].hex(), app['devicename']))

# DeregisterApp
# comfoconnect.cmd_deregister_app(bytes.fromhex('00000000000000000000000000000001'))

# VersionRequest
# version = comfoconnect.cmd_version_request()
# print(version)

# TimeRequest
# timeinfo = comfoconnect.cmd_time_request()
# print(timeinfo)

## Register sensors ################################################################################################

# comfoconnect.cmd_rpdo_request(SENSOR_FAN_NEXT_CHANGE)  # General: Countdown until next fan speed change
comfoconnect.cmd_rpdo_request(SENSOR_FAN_SPEED_MODE)  # Fans: Fan speed setting
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_SUPPLY_DUTY)  # Fans: Supply fan duty
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_EXHAUST_DUTY)  # Fans: Exhaust fan duty
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_SUPPLY_FLOW)  # Fans: Supply fan flow
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_EXHAUST_FLOW)  # Fans: Exhaust fan flow
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_SUPPLY_SPEED)  # Fans: Supply fan speed
# comfoconnect.cmd_rpdo_request(SENSOR_FAN_EXHAUST_SPEED)  # Fans: Exhaust fan speed
# comfoconnect.cmd_rpdo_request(SENSOR_POWER_CURRENT)  # Power Consumption: Current Ventilation
# comfoconnect.cmd_rpdo_request(SENSOR_POWER_TOTAL_YEAR)  # Power Consumption: Total year-to-date
# comfoconnect.cmd_rpdo_request(SENSOR_POWER_TOTAL)  # Power Consumption: Total from start
# comfoconnect.cmd_rpdo_request(SENSOR_DAYS_TO_REPLACE_FILTER)  # Days left before filters must be replaced
# comfoconnect.cmd_rpdo_request(SENSOR_AVOIDED_HEATING_CURRENT)  # Avoided Heating: Avoided actual
# comfoconnect.cmd_rpdo_request(SENSOR_AVOIDED_HEATING_TOTAL_YEAR)  # Avoided Heating: Avoided year-to-date
# comfoconnect.cmd_rpdo_request(SENSOR_AVOIDED_HEATING_TOTAL)  # Avoided Heating: Avoided total
# comfoconnect.cmd_rpdo_request(SENSOR_TEMPERATURE_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_TEMPERATURE_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_TEMPERATURE_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_TEMPERATURE_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_HUMIDITY_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_HUMIDITY_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_HUMIDITY_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
# comfoconnect.cmd_rpdo_request(SENSOR_HUMIDITY_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)

# Executing functions #########################################################################################

# comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)  # Go to auto mode
# comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)  # Set fan speed to 1
# comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)  # Set fan speed to 2
# comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)  # Set fan speed to 3

## Example interaction #########################################################################################

try:
    print('Waiting... Stop with CTRL+C')
    while True:
        # Callback messages will arrive in the callback method.
        sleep(1)

        if not comfoconnect.is_connected():
            print('We are not connected anymore...')

except KeyboardInterrupt:
    pass

## Closing the session #################################################################################################

comfoconnect.disconnect()
