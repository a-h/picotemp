cmake_minimum_required(VERSION 3.13)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(counter)

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

# Add pico_stdlib library which aggregates commonly used features.
target_link_libraries(main
  pico_stdlib
  hardware_pwm
  pico_cyw43_arch_none
)

# Add the UART.
pico_enable_stdio_usb(main 1)
pico_enable_stdio_uart(main 0)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)
