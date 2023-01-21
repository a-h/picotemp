#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"
#include <stdio.h>

int main() {
  stdio_init_all();

  const uint LED_PIN = CYW43_WL_GPIO_LED_PIN;
  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);

  while (true) {
    printf("Hello, world, updated!\n");
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(250);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(250);
  }
}
