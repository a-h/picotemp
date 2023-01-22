cmake_minimum_required(VERSION 3.13)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(picotemp C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

# Build...
# cd build
# cmake .. && make 

# Rest of project.
add_executable(main
    main.c
    # Can run these instead.
    # main_hello.c
    # irq.c
)
target_include_directories(main PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(main PRIVATE
	WIFI_SSID=\"${WIFI_SSID}\"
	WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
)

# Add pico_stdlib library which aggregates commonly used features.
target_link_libraries(main
  pico_stdlib
  hardware_pwm
  pico_cyw43_arch_lwip_threadsafe_background
  hardware_adc # required to read temperature
)

# Add the UART.
pico_enable_stdio_usb(main 1)
pico_enable_stdio_uart(main 0)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)
