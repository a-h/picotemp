#include "hardware/adc.h"
#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"
#include <stdio.h>

/* Choose 'C' for Celsius or 'F' for Fahrenheit. */
#define TEMPERATURE_UNITS 'C'

/* References for this implementation:
 * raspberry-pi-pico-c-sdk.pdf, Section '4.1.1. hardware_adc'
 * pico-examples/adc/adc_console/adc_console.c */
float read_onboard_temperature(const char unit) {
  /* 12-bit conversion, assume max value == ADC_VREF == 3.3 V */
  const float conversionFactor = 3.3f / (1 << 12);

  float adc = (float)adc_read() * conversionFactor;
  float tempC = 27.0f - (adc - 0.706f) / 0.001721f;

  if (unit == 'C') {
    return tempC;
  } else if (unit == 'F') {
    return tempC * 9 / 5 + 32;
  }

  return -1.0f;
}

int main() {
  // Initialize serial.
  stdio_init_all();

  // Initialize LED.
  const uint LED_PIN = CYW43_WL_GPIO_LED_PIN;
  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);

  // Initialize hardware AD converter, enable onboard temperature sensor and
  // select its channel (do this once for efficiency, but beware that this
  // is a global operation).
  adc_init();
  adc_set_temp_sensor_enabled(true);
  adc_select_input(4);

  while (true) {
    printf("Hello, world!\n");
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(250);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(250);
    float temperature = read_onboard_temperature(TEMPERATURE_UNITS);
    printf("Onboard temperature = %.02f %c\n", temperature, TEMPERATURE_UNITS);
  }
}
