import time
import network
import socket
from machine import Pin

class WebServer:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        
        self.led = False
        self.pump = False
        self.fan = False
    
#        self.ledState = 'LED State Unknown'
        self.temperature1 = 0.0
        self.temperature2 = 0.0
        self.temperature3 = 0.0
        self.temperature4 = 0.0
        self.humidity1 = 0.0
        self.humidity2 = 0.0
        self.humidity3 = 0.0
        self.humidity4 = 0.0
        self.water_level = 0.0
        self.light_intensity1 = 0.0
        self.light_intensity2 = 0.0
        
        self.html ="""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
        .buttonGreen { background-color: #4CAF50; border: 2px solid #000000; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
        .buttonRed { background-color: #D11D53; border: 2px solid #000000; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
        .button-container { display: inline-block; vertical-align: top; margin: 10px; }
    </style>
</head>
<body>
    <center><h2>Control Panel</h2></center>
    <form>
        <center>
            <div class="button-container">
                <button class="buttonGreen" name="pump" value="True" type="submit">Pump ON</button>
                <button class="buttonRed" name="pump" value="False" type="submit">Pump OFF</button>
            </div>
            <div class="button-container">
                <button class="buttonGreen" name="fan" value="True" type="submit">Fan ON</button>
                <button class="buttonRed" name="fan" value="False" type="submit">Fan OFF</button>
            </div>
            <div class="button-container">
                <button class="buttonGreen" name="led" value="True" type="submit">LED ON</button>
                <button class="buttonRed" name="led" value="False" type="submit">LED OFF</button>
            </div>
        </center>
    </form>

    <br><br>
    <center><h2>Sensor Readings</h2></center>
    <p>Temperature Sensor 1: %s°C</p>
    <p>Temperature Sensor 2: %s°C</p>
    <p>Temperature Sensor 3: %s°C</p>
    <p>Temperature Sensor 4: %s°C</p>
    <p>Humidity Sensor 1: %s</p>
    <p>Humidity Sensor 2: %s</p>
    <p>Humidity Sensor 3: %s</p>
    <p>Humidity Sensor 4: %s</p>
    <p>Sunlight Sensor 1: %s</p>
    <p>Sunlight Sensor 2: %s</p>
    <p>Water Level: %s</p>
    <br><br>
</body>
</html>

"""
    


    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        max_wait = 100
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
            
        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('Connected')
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )


    def start_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.server = socket.socket()
        self.server.bind(addr)
        self.server.listen(1)
        print('listening on', addr)


    def listen(self):
        try:       
            cl, addr = self.server.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
                
            
            # Create and send response
            
            temperature1 = self.temperature1
            temperature2 = self.temperature2
            temperature3 = self.temperature3
            temperature4 = self.temperature4
            humidity1 = self.humidity1
            humidity2 = self.humidity2
            humidity3 = self.humidity3
            humidity4 = self.humidity3
            
            water_level = self.water_level
            light_intensity1 = self.light_intensity1
            light_intensity2 = self.light_intensity2

            response = self.html % (temperature1, temperature2, temperature3, temperature4, humidity1, humidity2, humidity3, humidity4, light_intensity1, light_intensity2, water_level)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            
        except OSError as e:
            cl.close()
            print('connection closed')


    def set_temperature1(self, temperature1):
        self.temperature1 = temperature1
        
    def set_temperature2(self, temperature2):
        self.temperature2 = temperature2
        
    def set_temperature3(self, temperature3):
        self.temperature3 = temperature3
        
    def set_temperature4(self, temperature4):
        self.temperature4 = temperature4
        
    def set_humidity1(self, humidity1):
        self.humidity1 = humidity1
        
    def set_humidity2(self, humidity2):
        self.humidity2 = humidity2
        
    def set_humidity3(self, humidity3):
        self.humidity3 = humidity3
        
    def set_humidity4(self, humidity4):
        self.humidity4 = humidity4

    def set_light_intensity1(self, light_intensity1):
        self.light_intensity1 = light_intensity1
    
    def set_light_intensity2(self, light_intensity2):
        self.light_intensity2 = light_intensity2

    def set_water_level(self, water_level):
        self.water_level = water_level

    def run(self):
        self.connect_to_wifi()
        self.start_server()
        
# Usage example:
ssid = ''
password = ''
web_server = WebServer(ssid, password)


web_server.run()

while(True):
    web_server.listen()
    web_server.set_water_level(1.6)



