# PicoTemp

An MQTT based Raspberry Pi Pico W smart home temperature/humidity reader using a dht20 sensor, and a 32x128 OLED display.

NOTE: **Make sure that you create a `secrets.py` file before running!**

## Circuit

Here is the layout for the circuit.

![A circuit diagram](diagram.png "Made in Fritzing")

## Setting up Home Assistant/MQTT.

### Setting up with Docker Compose.

First, use the command `docker compose up` to run the `compose.yaml` file. This should create an instance of home-assistant running at [http://localhost:8123](http://localhost:8123). Log in with username: `user` and password: `12345`. It is already set up with an mqtt broker.

### Creating displays for MQTT data.

To create a display for the MQTT data, open the file `hass_config/configuration.yaml` and add an mqtt sensor like this:
```yaml
mqtt:
  sensor:
    - name: "Conservatory Temperature"
      state_topic: "home-assistant/conservatory-sensor/sensor"
      unit_of_measurement: "°C"
      value_template: "{{ value_json.temperature }}"
    - name: "Conservatory Humidity"
      state_topic: "home-assistant/conservatory-sensor/sensor"
      unit_of_measurement: "%"
      value_template: "{{ value_json.humidity }}"
```

## Guide

### Installing Thonny.

First, download Thonny (a free python IDE) from [https://thonny.org](https://thonny.org/).

### Configuring Thonny.

Now, open the Thonny editor. The first thing you should do is open the settings ( [Tools > Options] ) and open the 'Interpreter' tab. 
Then change the 'Which interpreter or device should Thonny use for running your code?' dropdown to 'MicroPython (Raspberry Pi Pico)'.

### Updating the Pico W.

It is now time to flash the software for MicroPython to the Raspberry Pi Pico. You can find it at [https://micropython.org/download/rp2-pico-w/](https://micropython.org/download/rp2-pico-w/). Click on the first link under 'Nightly builds'.

Once it is downloaded, plug in the raspberry pi pico while holding the 'BOOTSEL' button on the device. This should create a USB device called 'RPI-RP2'. Copy the downloded '.uf2' file to this USB drive. You should only need to do this once.

### Downloading and customizing the project.

Now it is time to download the code for the pico. It can be downloaded as a zip using [this link](https://github.com/a-h/picotemp/archive/refs/heads/main.zip). Once it is downloaded, extract the contents (on windows, right click and use 'extract' - don't double click!). 

Go back to Thonny and use [File > Open] to open `main.py` from the extracted files. Then use [File > Open] again to open `secrets_example.py`. If it is not already selected, click the `secrets_example.py` tab.

Now, replace the placeholders for the correct data. Once that is done, use [File > Save as...], replace the file name of `secrets_example.py` with `secrets.py` and click save.

### Running the project.

Make sure the pico is plugged in, then in Thonny, press the button labled 'STOP' to connect to the pico, then use [View > Files] which will open a side-panel showing the current folder on top, and the pico's storage below.

If there is anything in the pico's window, right click and press delete until the storage is empty. Now right click on the folder called 'lib' at the top and select 'Copy to /'. This might take a while!

Finally, right click on main.py and click 'Copy to /'. Do this again for secrets.py.

When you unplug the pico and plug it back in, it will run the program.
