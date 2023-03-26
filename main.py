import rp2
import network
import ubinascii
import machine
import time
import socket
from umqtt.simple import MQTTClient
from machine import Pin

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

last_message = 0
message_interval = 5
counter = 0

led = machine.Pin('LED', machine.Pin.OUT)

# Set country to avoid possible errors / https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/
rp2.country('GB')

# Enable WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Load login data from different file for safety reasons
ssid = secrets['wifi_ssid']
psk = secrets['wifi_psk']
broker = secrets['mqtt_broker']
port = secrets['mqtt_port']
topic_temp = secrets['mqtt_topic_temp']
topic_hum = secrets['mqtt_topic_hum']
username = secrets['mqtt_username']
password = secrets['mqtt_password']
clientID = ubinascii.hexlify(machine.unique_id())

# ([(ip, subnet, gateway, dns)])
wlan.ifconfig((secrets['wifi_ip'], secrets['wifi_subnet'], secrets['wifi_gateway'] , secrets['wifi_dns']))

if not wlan.isconnected():
    wlan.connect(ssid,psk)
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
    raise RuntimeError('WiFi connection failed! Expected status: 3, Actual status: ' + wlan.status())
else:
    status = wlan.ifconfig()
    print('Connected with IP of: ' + status[0])
    
### Topic Setup ###

def connect_and_subscribe():
  global client, mqtt_server, topic_sub
  client = MQTTClient(clientID, broker, port, username, password)
  client.connect()
  print('Connected to %s MQTT broker as client ID: %s' % (broker, client))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
      if (time.time() - last_message) > message_interval:
          reading = sensor_temp.read_u16() * conversion_factor
          temperature = 27 - (reading - 0.706)/0.001721
          pub_msg = str(temperature)
          client.publish(topic, pub_msg)
          last_message = time.time()
      time.sleep_ms(10)
  except OSError as e:
    restart_and_reconnect()
