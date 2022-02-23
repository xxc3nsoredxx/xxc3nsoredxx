if (TARGET tinyusb_device)
        add_executable(msc_dual_lun)

        target_sources(msc_dual_lun PUBLIC
                ${CMAKE_CURRENT_LIST_DIR}/main.c
                ${CMAKE_CURRENT_LIST_DIR}/msc_disk_dual.c
                ${CMAKE_CURRENT_LIST_DIR}/usb_descriptors.c
                )

        target_include_directories(msc_dual_lun PUBLIC
                ${CMAKE_CURRENT_LIST_DIR}
                )

        target_link_libraries(msc_dual_lun PUBLIC
                pico_stdlib
                tinyusb_device
                tinyusb_board
                )

        pico_add_extra_outputs(msc_dual_lun)
else ()
        message(WARNING "TinyUSB not found, ignoring msc_dual_lun!")
endif ()
