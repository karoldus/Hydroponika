import time
import board
import busio
import utime
from machine import Pin

# from adafruit_hcsr04 import HCSR04
from adafruit_tsl2591 import TSL2591
# from adafruit_bme280 import basic as adafruit_bme280
# import adafruit_bme680

I2C_0_SDA_PIN = board.GP0
I2C_0_SCL_PIN = board.GP1
I2C_1_SDA_PIN = board.GP2
I2C_1_SCL_PIN = board.GP3
# TODO add pinout...
TRIG_PIN = board.GP6
ECHO_PIN = board.GP7


led_pin = Pin("LED", Pin.OUT)
# trigger = Pin(TRIG_PIN, Pin.OUT)
# echo = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DOWN)

# HC-SR04 sensor
# sonar = HCSR04(trigger_pin=TRIG_PIN, echo_pin=ECHO_PIN)


# BME280 and BME680 sensors
i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c, address=0x77)
# bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c, address=0x76)
# bme280.sea_level_pressure = 1013.25
# bme680.sea_level_pressure = 1013.25

# def measure_distance():
#     trigger.low()
#     utime.sleep_us(2)
#     trigger.high()
#     utime.sleep_us(10)
#     trigger.low()
#     while echo.value() == 0:
#      pass

#     start_time = utime.ticks_us()

#     while echo.value() == 1:
#         pass

#     end_time = utime.ticks_us()
#     duration = utime.ticks_diff(end_time, start_time)
#     distance = duration / 58

#     return distance
"""
init TSL2591
"""
sensor = TSL2591(i2c)
while True:
    led_pin.toggle()
    # print(f"\nBME280: {round(bme280.temperature, 2)}C, {round(bme280.relative_humidity, 2)}%, {round(bme280.pressure, 2)}hPa, {round(bme280.altitude, 2)}m")
    # print(f"BME680: {round(bme680.temperature, 2)}C, {round(bme680.relative_humidity, 2)}%, {round(bme680.pressure, 2)}hPa, {round(bme680.altitude, 2)}m, {bme680.gas}ohm")
    # try:
    #     print((sonar.distance,))
    # except RuntimeError:
    #     print("Retrying!")
    #     pass
    time.sleep(2)
    # dist = measure_distance()
    # print("Odległość:", dist, "cm")
    """
    Measuring light level example
    """
    # Read and calculate the light level in lux.
    lux = sensor.lux
    print("Total light: {0}lux".format(lux))
    # You can also read the raw infrared and visible light levels.
    # These are unsigned, the higher the number the more light of that type.
    # There are no units like lux.
    # Infrared levels range from 0-65535 (16-bit)
    infrared = sensor.infrared
    print("Infrared light: {0}".format(infrared))
    # Visible-only levels range from 0-2147483647 (32-bit)
    visible = sensor.visible
    print("Visible light: {0}".format(visible))
    # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
    full_spectrum = sensor.full_spectrum
    print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
    time.sleep(1.0)
