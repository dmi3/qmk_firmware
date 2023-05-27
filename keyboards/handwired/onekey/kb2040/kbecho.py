#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/qmk/qmk_firmware/blob/master/docs/feature_rawhid.md
# https://gist.github.com/fauxpark/03a3efcc7dbdfbfe57791ea267b13c55

# sudo pip install hid==1.0.4
# sudo nano /etc/udev/rules.d/50-macro.conf
# SUBSYSTEM=="usb", ATTRS{idVendor}=="0xfeed", ATTR{idProduct}=="0x6465", MODE="0666"

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
    send_raw_packet(sys.argv[1][:32].encode('ascii', 'replace'))
