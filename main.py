import time
import board
import busio
import utime
from machine import Pin

# from adafruit_bme280 import basic as adafruit_bme280
# import adafruit_bme680

I2C_0_SDA_PIN = board.GP0
I2C_0_SCL_PIN = board.GP1
I2C_1_SDA_PIN = board.GP2
I2C_1_SCL_PIN = board.GP3
# TODO add pinout...
TRIG_PIN = 16
ECHO_PIN = 17


led_pin = Pin("LED", Pin.OUT)
trigger = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DOWN)


# BME280 and BME680 sensors
# i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c, address=0x77)
# bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c, address=0x76)
# bme280.sea_level_pressure = 1013.25
# bme680.sea_level_pressure = 1013.25

while True:
    led_pin.toggle()
    # print(f"\nBME280: {round(bme280.temperature, 2)}C, {round(bme280.relative_humidity, 2)}%, {round(bme280.pressure, 2)}hPa, {round(bme280.altitude, 2)}m")
    # print(f"BME680: {round(bme680.temperature, 2)}C, {round(bme680.relative_humidity, 2)}%, {round(bme680.pressure, 2)}hPa, {round(bme680.altitude, 2)}m, {bme680.gas}ohm")
    time.sleep(2)
    dist = measure_distance()
    print("Odległość:", dist, "cm")
    
def measure_distance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    while echo.value() == 0:    
     pass

    start_time = utime.ticks_us()

    while echo.value() == 1:
        pass
        
    end_time = utime.ticks_us()
    duration = utime.ticks_diff(end_time, start_time)
    distance = duration / 58

    return distance
