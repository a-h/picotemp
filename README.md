# Picotemp

PicoW temperature sensor.

## Tasks

### build

```
cmake -DWIFI_SSID=${WIFI_SSID} -DWIFI_PASSWORD=${WIFI_PASSWORD} -DPICO_BOARD=pico_w . && make
```

### upload

```
picotool load -f ./main.uf2
```

### flash

Requires: build, upload

### serial

```
minicom --device=/dev/tty.usbmodem21301
```
