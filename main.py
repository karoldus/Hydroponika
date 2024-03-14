# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_bme680

# Create sensor object, using the board's default I2C bus.
i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c, address=0x77)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c, address=0x76)

# OR create sensor object, using the board's default SPI bus.
# spi = busio.SPI(board.GP2, MISO=board.GP0, MOSI=board.GP3)
# bme_cs = digitalio.DigitalInOut(board.GP1)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25
bme680.sea_level_pressure = 1013.25

while True:
    print(f"\nBME280: {round(bme280.temperature, 2)}C, {round(bme280.relative_humidity, 2)}%, {round(bme280.pressure, 2)}hPa, {round(bme280.altitude, 2)}m")
    print(f"BME680: {round(bme680.temperature, 2)}C, {round(bme680.relative_humidity, 2)}%, {round(bme680.pressure, 2)}hPa, {round(bme680.altitude, 2)}m, {bme680.gas}ohm")
    time.sleep(2)