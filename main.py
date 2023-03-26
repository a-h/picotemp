import rp2
import network
import ubinascii
import machine
import time
import socket

# Sensor library.
import dht

# OLED library.
from oled import ssd1306,gfx

# MQTT library.
from umqtt.simple import MQTTClient
from machine import Pin, I2C

# secrets.py
from secrets import secrets

# Configure the DHT22 sensor. This sensor reads temperature and humidity.
sensor = dht.DHT22(Pin(2))

# Configure the I2C OLED display.
i2c = I2C(0,sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Test the display with a message.
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

# Display a message.
display.fill(0)
display.text('Network Init!', 0, 0, 1)
display.invert(False)
display.show()

# Secret information is loaded from secrets.py - see secrets_example.py
ssid = secrets['wifi_ssid']
psk = secrets['wifi_psk']
broker = secrets['mqtt_broker']
port = secrets['mqtt_port']
topic = secrets['mqtt_topic']
username = secrets['mqtt_user']
password = secrets['mqtt_password']
clientID = ubinascii.hexlify(machine.unique_id())

# Write a message to the display.
display.fill(0)
display.text('Secrets Imported!', 0, 0, 1)
display.invert(False)
display.show()

# Configure the Wifi connection settings.
wlan.ifconfig((secrets['wifi_ip'], secrets['wifi_subnet'], secrets['wifi_gateway'] , secrets['wifi_dns'])) # ([(ip, subnet, gateway, dns)])

# Write a message on the display.
display.fill(0)
display.text('WiFi Configured!', 0, 0, 1)
display.invert(False)
display.show()

if not wlan.isconnected():
    wlan.connect(ssid,psk) # Connect to the wifi.
    
    # Display a message on the display.
    display.fill(0)
    display.text('WiFi Connecting...', 0, 0, 1)
    display.invert(False)
    display.show()
    
    # Wait for the connection.
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
    # Wifi Failure!
    
    # Display a message to the display.
    display.fill(0)
    display.text('Wifi Failed!', 0, 0, 1)
    display.text('Error code: '+ wlan.status(), 0, 10, 1)
    display.invert(True)
    display.show()
    
    # Return an error.
    raise RuntimeError('WiFi connection failed! Expected status: 3, Actual status: ' + wlan.status())
else:
    # Wifi Success!
    status = wlan.ifconfig() # Get the IP address.
    print('Connected with IP of:' + status[0])
    
    # Display a message to the display.
    display.fill(0)
    display.text('Wifi Connected!', 0, 0, 1)
    display.text('IP Address:',0,10,1)
    display.text(status[0], 0, 20, 1)
    display.invert(False)
    display.show()
    
# Connecting to MQTT:

def connect_and_subscribe():
  global client, mqtt_server # Theese variables are available outside this function.
  client = MQTTClient(clientID, broker, port, username, password) # Configure the MQTT settings.
  client.connect() # Connect to the MQTT broker.
  
  print('Connected to %s MQTT broker as client ID: %s' % (broker, client))
  
  # Write a message to the display confirming the MQTT connection.
  display.fill(0)
  display.text('MQTT Connected!', 0, 0, 1)
  display.text('Broker IP:', 0, 10, 1)
  display.text(broker,0,18,1)
  display.invert(False)
  display.show()
  
  return client

# If there is an error, display a message and then restart from the beginning.
def restart_and_reconnect():
  # Write the message.
  display.fill(0)
  display.text('Error!', 0, 0, 1)
  display.text("Resetting...", 0, 10, 1)
  display.invert(True)
  display.show()
  
  # Wait so the error can be read.
  time.sleep(10)
  
  # Restart from the top.
  machine.reset()

try:
  client = connect_and_subscribe() # Connect to the MQTT broker.
except OSError as e:
  restart_and_reconnect() # If there is an error, reset and try again.

# The main loop:

while True: # Forever.
  try:
      # If the time since the last message has been longer than the interval, send a message and update the display.
      if (time.time() - last_message) > message_interval:
          # Tell the sensor to take a measurement.
          sensor.measure()
          
          # Get the sensor results
          temperature = sensor.temperature()
          temp_pub_msg = str(temperature)
          hum = sensor.humidity()
          hum_pub_msg = str(hum)
          
          # Turn into json for publishing.
          client.publish(topic, '{"temperature": %f,"humidity": %f}' % (temperature,hum))
          
          # Get the current IP for the display.
          status = wlan.ifconfig()
          
          # Initialise the graphics drawer.
          graphics = gfx.GFX(128, 32, display.pixel)
          
          # Draw the screen.
          display.fill(0) # Clear the screen
          display.text(status[0], 0, 0, 1) # Draw the current IP in the top left.
          graphics.hline(0,8,128,1) # Draw a horizontal line with x=0, y=8, width=128 (the width of the screen) and the color of 1 (white).
          display.text("Temp.: " + str(temperature) + "C", 0, 10, 1) # Draw the temperature with a 'C' on the end.
          display.text("Humidity: " + str(hum) + "%", 0, 20, 1) # Draw the humidity with a '%' on the end.
          display.invert(False) # Do not invert the colors.
          display.show() # Write the changes to the display.
           
          last_message = time.time() # Store the last time the display/MQTT was updated.
      time.sleep_ms(10) # Check the time every 10 milliseconds.
  except OSError as e:
    restart_and_reconnect() # If there is an error, reset the device and try again.
