#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/qmk/qmk_firmware/blob/master/docs/feature_rawhid.md
# https://gist.github.com/fauxpark/03a3efcc7dbdfbfe57791ea267b13c55

# sudo pip install hid==1.0.4
# sudo apt-get install libhidapi-hidraw0 libhidapi-libusb0
# sudo nano /etc/udev/rules.d/50-macro.rules
# KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="feed", MODE="0666"
# sudo udevadm control --reload-rules && udevadm trigger

import sys
import hid

vendor_id  = 0xfeed
product_id = 0x6465

usage_page = 0xFF60
usage      = 0x61

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    # usage_page is always zero
    # https://github.com/apmorton/pyhidapi/issues/38
    #raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]
    raw_hid_interfaces = [i for i in device_interfaces if i['interface_number'] == 1]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    print("Manufacturer: %s" % interface.manufacturer)
    print("Product: %s" % interface.product)

    return interface

def send_raw_packet(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * 33 # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_packet = bytes(request_data)

    print("Request:")
    print(request_packet)

    try:
        interface.write(request_packet)

        response_packet = interface.read(32, timeout=1000)

        print("Response:")
        print(response_packet)
    finally:
        interface.close()

if __name__ == '__main__':
    if not sys.argv[1] in ['t', 'p', 'l'] or (len(sys.argv) <= 2 and sys.argv[1] != "l"):
        print("Usage:\n  kbecho.py t text # Echo text\n  kbecho.py p 55 # Show percent (progress)\n  kbecho.py l # Show logo")
        exit(1)

    data = str(" ".join(sys.argv[1:])).replace("\\n", "\n")[:30].encode('ascii', 'replace')
    send_raw_packet(data)
