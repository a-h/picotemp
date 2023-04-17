# Engineering workshop

Adrian Hesketh

@adrianhesketh

https://adrianhesketh.com

https://infinityworks.com

---

# Microcontrollers

* Can be programmed to perform specific tasks
* Responds to different inputs, like sensors that detect changes in the environment
* Often used in devices that need to be automated or require precise control
* Helps make devices work more efficiently and accurately
* Embedded in many products and devices, such as console controllers

---

# Raspberry Pi Pico

- Can control other hardware components and interact with the physical world
- Can be programmed in a variety of languages, including Micropython and C
- Has GPIO (General Purpose Input/Output) support that can be used to interface with external devices and sensors
- Affordable
- Expandable using a range of add-on boards and sensors

---

# Micropython?

Variant of Python, optimized for use in embedded systems.

- **Interactive Shell:** You can type in commands and see the results immediately. Easy to test and debug.
- **Small Memory Footprint:** Uses less RAM than normal Python.
- **Built-in Libraries:** Includes libraries to provide access to hardware features, like GPIO.
- **Easy to Learn:** Based on Python, which is easier to work with than C.
- **Open Source:** Micropython is open-source.

---

# How code runs on a Raspberry Pi Pico using Micropython

- Write code in Micropython and save it to your computer (Thonny)
- Transfer the code to the Pico microcontroller using a USB cable
- The Pico's built-in processor runs the Micropython interpreter
- The interpreter reads your code and converts it into machine-readable instructions
- The Pico's processor executes the instructions and carries out the tasks specified by your code
- Your code can interact with hardware connected to the Pico's GPIO pins, like turning on an LED or reading sensor data

---

# Workshop: Exercises

* Use Python on your laptop to print "SOS" as Morse code dots and dashes on the screen of your laptop.
* Install Thonny, and setup your Pico.
* Adapt the code to run on the Pico, and to print "SOS" to the serial connection.
* Adapt the code to also flash the built-in LED to transmit the morse code.

---

# Python example

```python
import time

sos = '... --- ...'

while True:
  for symbol in sos:
    if symbol == '.':
      print('.', end='', flush=True)
      time.sleep(0.2)
    elif symbol == '-':
      print('-', end='', flush=True)
      time.sleep(0.5)
    else:
      print(' ', end='', flush=True)
      time.sleep(0.5)
  time.sleep(1)
  print('\n')
```

---

# Inputs (sensors)

- **Temperature**: measure temperature
- **Humidity**: measure relative humidity
- **Light**: measure light intensity
- **Proximity**: detect nearby objects
- **Accelerometers**: measure acceleration
- **Gyroscopes**: measure rotational movement
- **Magnetometers**: measure magnetic fields
- **Pressure**: measure pressure
- **Gas**: detect presence of gases
- **Biometric**: heart rate, blood pressure, fingerprint patterns

---

# Outputs

- **LEDs**: visual signaling, status indication, displays
- **LCD displays**: text and graphical displays
- **Buzzers and speakers**: audible signaling, alarms, sound effects
- **Motors**: motion control, robotics, automation
- **Servos**: precise angular positioning
- **Solenoids**: actuation, valves, locks, latches
- **Relays**: switching high voltage/current loads
- **Displays**: seven-segment, OLED, e-paper
- **Communication modules**: Wi-Fi, Bluetooth, serial connections

---
layout: image
---

<img src="sensors.jpg" style="height: 100%"/>

---

# GPIO

- Programmable to read or write digital signals
- Can receive or send a signal
- As input: detect voltage, receive data from sensors/devices
- As output: send voltage, control hardware components
- Common in microcontroller projects
- Example uses: read temperature data, control LED brightness

---

# Pinout

<img src="picow-pinout.svg" style="height: 95%"/>

---

# Digital high/low

<img src="/highlow.svg" style="width: 100%; height: 100%;" />

---

# Workshop: Soldering

* Wear safety glasses.
* Put the iron in the stand when you're not using it.
* Don't burn yourself.
* Don't burn other people.
  * If you burn yourself, put your hand under the cold water tap.
* Don't inhale the fumes.
* The stuff you solder will be hot too!
* Wires get hot if you put a soldering iron on them.

---

# Workshop: External LED breadboard assembly

* Connect LED to 3.3v (long side is +)
* Connect 10k resistor to ground

```python
import machine
led = machine.Pin(28, machine.Pin.OUT)
```

* Light up an LED with the 3.3v output.
* Control the LED with a GPIO.
* https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf
* https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf
* Install unstable Micropython for the LED example.

---

# Workshop: Assemble breadboard

<img src="diagram.png" style="height: 95%"/>

---

# Workshop: Get temp reading and send via serial

```python
from machine import Pin, I2C
import time

# Sensor library.
from dht20 import DHT20

# Configure the DHT20 sensor. This sensor reads temperature and humidity.
i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
dht20 = DHT20(0x38, i2c1) # 0x38 is a hex number.

while True:
  measurements = dht20.measurements
  
  temp = measurements['t'] # Temperature
  hum = measurements['rh'] # Relative Humidity
  print('temp: %f, hum: %f' % (temp, hum))

          
  time.sleep(1) # Check the time every second.
```

---

# Workshop: Write to an i2c display

```python
from machine import Pin, I2C

from oled import ssd1306,gfx

# Configure the I2C OLED display.
i2c = I2C(0,sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Test the display with a message.
display.text('Hello, World!', 0, 0, 1)
display.show()

while True:
  pass # Do nothing.
```

---

# Docker / Containers

* Docker: Popular platform for containerization
* Containers: Lightweight, portable, and self-sufficient units for software deployment

---

# Docker examples

* Run Alpine Linux (`docker run alpine:latest`)
* Run Apache (`docker run httpd:latest`)
* Run MongoDB (`docker run mongodb:latest`)

---

# Docker compose

```mermaid
graph LR;
Browser --> Web[Web Server];
Web --> Database;
```

```
docker compose up
docker compose down
```

---

# Final boss

* Get this code up and running...
* https://github.com/a-h/picotemp

---

# Final boss - 2nd health bar

* Assemble your PCB
