import time
import network
import socket
from machine import Pin

class WebServer:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.led = Pin("LED", Pin.OUT)
        self.ledState = 'LED State Unknown'
        self.temperature1 = 0.0
        self.temperature2 = 0.0
        self.water_level = "Unknown"
        self.light_intensity = "Unkonown"
        self.html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><center><h2>Control Panel</h2></center><br><br>
<form><center>
<center> <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
<br><br>
<center> <button class="buttonRed" name="led" value="off" type="submit">LED OFF</button>
</form>
<p>%s<p>
<br><br>
<center><h2>Sensor Readings</h2></center>
<p>Temperature Sensor 1: %s°C</p>
<p>Temperature Sensor 2: %s°C</p>
<p>Water Level: %s</p>
<p>Light Intensity: %s</p>
<br><br>
</body></html>
"""
    


    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        max_wait = 10
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
        while True:
            try:       
                cl, addr = self.server.accept()
                print('client connected from', addr)
                request = cl.recv(1024)
                print("request:")
                print(request)
                request = str(request)
                led_on = request.find('led=on')
                led_off = request.find('led=off')
                
                print( 'led on = ' + str(led_on))
                print( 'led off = ' + str(led_off))
                
                if led_on == 8:
                    print("led on")
                    self.led.on()
                    time.sleep(1)
                    self.ledState = "LED is ON"
                if led_off == 8:
                    self.led.off()
                    print("led off")
                    self.ledState = "LED is OFF"
                
                
                # Create and send response
                
                stateis = self.ledState
                temperature1 = self.temperature1
                temperature2 = self.temperature2
                water_level = self.water_level
                light_intensity = self.light_intensity

                response = self.html % (stateis, temperature1, temperature2, water_level, light_intensity)
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()
                
            except OSError as e:
                cl.close()
                print('connection closed')


    def set_temperature(self, temperature1, temperature2):
        self.temperature1 = temperature1
        self.temperature2 = temperature2


    def set_light_intensity(self, light_intensity):
        self.light_intensity = light_intensity

    
    def set_water_level(self, water_level):
        self.water_level = water_level


    def run(self):
        self.connect_to_wifi()
        self.start_server()
        self.listen()

# # Usage example:
# ssid = ''
# password = ''
# web_server = WebServer(ssid, password)
# web_server.run()
