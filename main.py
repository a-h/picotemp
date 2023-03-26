import rp2
import network
import ubinascii
import machine
import time
import socket
import dht

from oled import ssd1306,gfx

from umqtt.simple import MQTTClient
from machine import Pin, I2C
from secrets import secrets

# Configure the DHT22 sensor. This sensor reads temperature and humidity.
sensor = dht.DHT22(Pin(2))

# Configure the I2C OLED display.
i2c = I2C(0,sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

display.text('Display Init!', 0, 0, 1)
display.invert(False)
display.show()

# Count how often messages are sent - one every 5 seconds.
last_message = 0
message_interval = 5
counter = 0

# Set country to avoid possible errors / https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/
rp2.country('GB')

# Enable WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

display.fill(0)
display.text('Network Init!', 0, 0, 1)
display.invert(False)
display.show()

# Load login data from different file for safety reasons
ssid = secrets['wifi_ssid']
psk = secrets['wifi_psk']
broker = secrets['mqtt_broker']
port = secrets['mqtt_port']
topic_temp = secrets['mqtt_topic_temp']
topic_hum = secrets['mqtt_topic_hum']
username = secrets['mqtt_user']
password = secrets['mqtt_password']
clientID = ubinascii.hexlify(machine.unique_id())

display.fill(0)
display.text('Secrets Imported!', 0, 0, 1)
display.invert(False)
display.show()

# ([(ip, subnet, gateway, dns)])
wlan.ifconfig((secrets['wifi_ip'], secrets['wifi_subnet'], secrets['wifi_gateway'] , secrets['wifi_dns']))

display.fill(0)
display.text('WiFi Configured!', 0, 0, 1)
display.invert(False)
display.show()

if not wlan.isconnected():
    wlan.connect(ssid,psk)
    display.fill(0)
    display.text('WiFi Connecting...', 0, 0, 1)
    display.invert(False)
    display.show()
    while not wlan.isconnected():
        machine.idle() # If the WiFi is not connected yet, save power.

# Wait for connection with 10 second timeout
wifiTimeout = 10
print('Waiting for WiFi connection.', end="") # Don't create a newline when printing this text.
while wifiTimeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wifiTimeout -= 1
    print(".", end="") # Don't create a newline when printing this text either.
    time.sleep(1)
print("") # Create a newline

# Possible WiFi Connection Errors:
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

if wlan.status() != 3:
    display.fill(0)
    display.text('Wifi Failed!', 0, 0, 1)
    display.text('Error code: '+ wlan.status(), 0, 10, 1)
    display.invert(True)
    display.show()
    raise RuntimeError('WiFi connection failed! Expected status: 3, Actual status: ' + wlan.status())
else:
    status = wlan.ifconfig()
    print('Connected with IP of:' + status[0])
    display.fill(0)
    display.text('Wifi Connected!', 0, 0, 1)
    display.text('IP Address:',0,10,1)
    display.text(status[0], 0, 20, 1)
    display.invert(False)
    display.show()
    
### Topic Setup ###

def connect_and_subscribe():
  global client, mqtt_server
  client = MQTTClient(clientID, broker, port, username, password)
  client.connect()
  print('Connected to %s MQTT broker as client ID: %s' % (broker, client))
  display.fill(0)
  display.text('MQTT Connected!', 0, 0, 1)
  display.text('Broker IP:', 0, 10, 1)
  display.text(broker,0,18,1)
  display.invert(False)
  display.show()
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  display.fill(0)
  display.text('MQTT Failed!', 0, 0, 1)
  display.text("Retrying...", 0, 10, 1)
  display.invert(True)
  display.show()
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
      if (time.time() - last_message) > message_interval:
          sensor.measure()
          
          temperature = sensor.temperature()
          temp_pub_msg = str(temperature)
          client.publish(topic_temp, temp_pub_msg)
          
          hum = sensor.humidity()
          hum_pub_msg = str(hum)
          client.publish(topic_hum, hum_pub_msg)
          
          graphics = gfx.GFX(128, 32, display.pixel)
          status = wlan.ifconfig()
          display.fill(0)
          display.text(status[0], 0, 0, 1)
          graphics.hline(0,8,128,1) # x,y,width,color
          display.text("Temp.: " + str(temperature) + "C", 0, 10, 1)
          display.text("Humidity: " + str(hum) + "%", 0, 20, 1)
          display.invert(False)
          display.show()
          
          last_message = time.time()
      time.sleep_ms(10)
  except OSError as e:
    restart_and_reconnect()
