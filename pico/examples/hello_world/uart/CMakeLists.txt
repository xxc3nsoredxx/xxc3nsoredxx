add_executable(hello_uart
        hello_uart.c
        )

# pull in common dependencies
target_link_libraries(hello_uart pico_stdlib)

# create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(hello_uart)
