from lib import hcsr04

sensor = hcsr04.HCSR04(trigger_pin=6, echo_pin=7, echo_timeout_us=10000)

try:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
except OSError as ex:
    print('ERROR getting distance:', ex)
