# Picotemp

PicoW temperature sensor.

## Tasks

### build

```
cmake -DPICO_BOARD=pico_w . && make
```

### upload

```
picotool load -f ./main.uf2
```

### flash

Requires: build, upload

