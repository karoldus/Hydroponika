import time
import board
import busio
import utime
from machine import Pin

from adafruit_bme280 import basic as adafruit_bme280
import adafruit_bme680
from adafruit_tsl2591 import TSL2591
from lib import hcsr04

I2C_0_SDA_PIN = board.GP0
I2C_0_SCL_PIN = board.GP1
I2C_1_SDA_PIN = board.GP2
I2C_1_SCL_PIN = board.GP3
# TODO add pinout...
TRIG_PIN = 6
ECHO_PIN = 7

LED_MOSFET_PIN = 8
WIND_MOSFET_PIN = 9
PUMP_MOSFET_PIN = 10

if __name__ == "__main__":

    #HC-SR04 sensor
    hcsr04_0 = hcsr04.HCSR04(trigger_pin=TRIG_PIN, echo_pin=ECHO_PIN, echo_timeout_us=10000)

    # I2C
    i2c_0 = busio.I2C(I2C_0_SCL_PIN, I2C_0_SDA_PIN)
    i2c_1 = busio.I2C(I2C_1_SCL_PIN, I2C_1_SDA_PIN)

    # BME280 and BME680 sensors
    bme280_0 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c_0, address=0x77)
    bme280_1 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c_1, address=0x77)
    bme280_0.sea_level_pressure = 1013.25
    bme280_1.sea_level_pressure = 1013.25

    bme680_0 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c_0, address=0x76)
    bme680_1 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c_1, address=0x76)
    bme680_0.sea_level_pressure = 1013.25
    bme680_1.sea_level_pressure = 1013.25

    # TSL2591 sensor
    tsl2591_0 = TSL2591(i2c_0)
    tsl2591_1 = TSL2591(i2c_1)

    led_buildin_pin = Pin("LED", Pin.OUT)

    led_pin = Pin(LED_MOSFET_PIN, Pin.OUT)
    wind_pin = Pin(WIND_MOSFET_PIN, Pin.OUT)
    pump_pin = Pin(PUMP_MOSFET_PIN, Pin.OUT)


    def measure_all():
        try:
            distance = hcsr04_0.distance_cm()
            print('Distance:', distance, 'cm')
        except OSError as ex:
            print('ERROR getting distance:', ex)
        
            # print(f"\nBME280: {round(bme280.temperature, 2)}C, {round(bme280.relative_humidity, 2)}%, {round(bme280.pressure, 2)}hPa, {round(bme280.altitude, 2)}m")
        # print(f"BME680: {round(bme680.temperature, 2)}C, {round(bme680.relative_humidity, 2)}%, {round(bme680.pressure, 2)}hPa, {round(bme680.altitude, 2)}m, {bme680.gas}ohm")
        # try:
        #     print((sonar.distance,))
        # except RuntimeError:
        #     print("Retrying!")
        #     pass

        print('BME280_0:', round(bme280_0.temperature, 2), '*C, ', round(bme280_0.relative_humidity, 2), "%, ", round(bme280_0.pressure, 2), 'hPa')
        print('BME280_1:', round(bme280_1.temperature, 2), '*C, ', round(bme280_1.relative_humidity, 2), "%, ", round(bme280_1.pressure, 2), 'hPa')
        print('BME680_0:', round(bme680_0.temperature, 2), '*C, ', round(bme680_0.relative_humidity, 2), "%, ", round(bme680_0.pressure, 2), 'hPa')
        print('BME680_1:', round(bme680_1.temperature, 2), '*C, ', round(bme680_1.relative_humidity, 2), "%, ", round(bme680_1.pressure, 2), 'hPa')
        print('TSL2591_0:', round(tsl2591_0.lux, 2))
        print('TSL2591_1:', round(tsl2591_1.lux, 2))
        print('-----------------------------------')

    led_pin.value(1)
    wind_pin.value(1)
    pump_pin.value(1)

    while True:
        led_buildin_pin.toggle()
        measure_all()
        time.sleep(10)

        # led_pin.toggle()
        # wind_pin.toggle()
        # pump_pin.toggle()

        # time.sleep(5)

        # led_pin.toggle()
        # wind_pin.toggle()
        # pump_pin.toggle()
        

