import time
import board
import busio
import utime
from machine import Pin, PWM
# from WebServer import WebServer


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

MAX_DISTANCE_CM = 9 

# def pin_slow_on(pwm_pin_obj, on_time_ms):
#     pwm_pin_obj.duty_u16(0)
#     for i in range(0, 65535, 65535//on_time_ms):
#         pwm_pin_obj.duty_u16(i)
#         utime.sleep_ms(1)
#     pwm_pin_obj.duty_u16(65535)

# def pin_slow_off(pwm_pin_obj, off_time_ms):
#     pwm_pin_obj.duty_u16(65535)
#     for i in range(65535, 0, -65535//off_time_ms):
#         pwm_pin_obj.duty_u16(i)
#         utime.sleep_ms(1)
#     pwm_pin_obj.duty_u16(0)
    
# def toggle_pump_test(pwm_pin_ob):
#     if pwm_pin_ob.duty_u16() == 0:
#         pin_slow_on(pwm_pin_ob, 200)
#     else:
#         pin_slow_off(pwm_pin_ob, 200)


# ssid = 'iPhone(Tadeusz)'
# password = 'abc2468d'
# web_server = WebServer(ssid, password)


# web_server.run()

# while True:
#     led_buildin_pin.toggle()
#     measure_all()

#     temperature1 = round(bme280_0.temperature, 2)
#     temperature2 = round(bme280_1.temperature, 2)
#     temperature3 = round(bme680_0.temperature, 2)
#     temperature4 = round(bme680_1.temperature, 2)
#     humidity1 = round(bme280_0.relative_humidity, 2)
#     humidity2 = round(bme280_1.relative_humidity, 2)
#     humidity3 = round(bme680_0.relative_humidity, 2)
#     humidity4 = round(bme680_1.relative_humidity, 2)
#     water_level = hcsr04_0.distance_cm()
#     light_intensity1 = round(tsl2591_0.lux, 2)
#     light_intensity2 = round(tsl2591_1.lux, 2)

#     web_server.set_temperature1(temperature1)
#     web_server.set_temperature2(temperature2)
#     web_server.set_temperature3(temperature3)
#     web_server.set_temperature4(temperature4)

#     web_server.set_humidity1(humidity1)
#     web_server.set_humidity2(humidity1)
#     web_server.set_humidity3(humidity1)
#     web_server.set_humidity4(humidity1)

#     web_server.set_light_intensity1(light_intensity1)
#     web_server.set_light_intensity2(light_intensity2)
#     web_server.set_water_level(water_level)
    
#     web_server.listen()
#     time.sleep(10)


def main():
    #HC-SR04 sensor
    hcsr04_0 = hcsr04.HCSR04(trigger_pin=TRIG_PIN, echo_pin=ECHO_PIN, echo_timeout_us=10000)

    # I2C
    i2c_0 = busio.I2C(I2C_0_SCL_PIN, I2C_0_SDA_PIN)
    i2c_1 = busio.I2C(I2C_1_SCL_PIN, I2C_1_SDA_PIN)

    # BME280 and BME680 sensors
    bme280_0 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c_0, address=0x77)
    #bme280_1 = adafruit_bme280.Adafruit_BME280_I2C(i2c=i2c_1, address=0x77)
    bme280_0.sea_level_pressure = 1013.25
    #bme280_1.sea_level_pressure = 1013.25

    bme680_0 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c_0, address=0x76)
   # bme680_1 = adafruit_bme680.Adafruit_BME680_I2C(i2c=i2c_1, address=0x76)
    bme680_0.sea_level_pressure = 1013.25
    #bme680_1.sea_level_pressure = 1013.25

    # TSL2591 sensor
    tsl2591_0 = TSL2591(i2c_0)
    tsl2591_1 = TSL2591(i2c_1)

    led_buildin_pin = Pin("LED", Pin.OUT)

    led_pin = Pin(LED_MOSFET_PIN, Pin.OUT)
    wind_pin = Pin(WIND_MOSFET_PIN, Pin.OUT)
    # pump_pin = Pin(PUMP_MOSFET_PIN, Pin.OUT) 
    pump_pwm = PWM(Pin(PUMP_MOSFET_PIN), freq=1000, duty_u16=0) # TODO freq może można zwiększyć?
    led_pin.value(0)
    wind_pin.value(0)
    def measure_all():
        try:
            distance = hcsr04_0.distance_cm()
            print('Distance:', distance, 'cm')
        except OSError as ex:
            print('ERROR getting distance:', ex)

        print('BME280_0:', round(bme280_0.temperature, 2), '*C, ', round(bme280_0.relative_humidity, 2), "%, ", round(bme280_0.pressure, 2), 'hPa')
       # print('BME280_1:', round(bme280_1.temperature, 2), '*C, ', round(bme280_1.relative_humidity, 2), "%, ", round(bme280_1.pressure, 2), 'hPa')
        print('BME680_0:', round(bme680_0.temperature, 2), '*C, ', round(bme680_0.relative_humidity, 2), "%, ", round(bme680_0.pressure, 2), 'hPa')
     #   print('BME680_1:', round(bme680_1.temperature, 2), '*C, ', round(bme680_1.relative_humidity, 2), "%, ", round(bme680_1.pressure, 2), 'hPa')
        print('TSL2591_0:', round(tsl2591_0.lux, 2))
       # print('TSL2591_1:', round(tsl2591_1.lux, 2))
        print('-----------------------------------')

    set_humidity = 75
    last_error = 0
    total_error = 0
    Kp = 5000
    Kd = 100
    Ki = 3000

    while True:
        measure_all()

        distance = hcsr04_0.distance_cm()
        print('Distance:', distance, 'cm')

        if distance > MAX_DISTANCE_CM:
            print("Napełnij zbiornik!")
            pump_pwm.duty_u16(0)
            time.sleep(300)
            continue
        if MAX_DISTANCE_CM > distance and distance > MAX_DISTANCE_CM - MAX_DISTANCE_CM * (1/3):
            print("niski poziom wody!")

         #humidity = (int(bme680_0.relative_humidity) + int(bme680_1.relative_humidity)) / 2 

        humidity = int(bme680_0.relative_humidity)
        # PID
        error = set_humidity - humidity
        proporional = error * Kp
        derivative = (error - last_error) * Kd
        integral = (error + last_error) * Ki
        u = proporional + derivative + integral
        if integral > 65535:
            integral = 65535
            u = 65535
           
        if integral < 0:
            integral = 0
            u = 0
        if error < 2:
            u = 0
        # wystawianie pwm dla wyjścia pompy
        pump_pwm.duty_u16(int(u))
        print(u)
        print(integral)
        print(humidity)
        
        last_error = error
        
        


        

if __name__ == '__main__':
    main()
