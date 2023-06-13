#!/usr/bin/env python

import sys


def calculate_prefix(ip_address, subnet_mask):
    ip_octets = ip_address.split('.')
    subnet_octets = subnet_mask.split('.')
    prefix = 0
    for ip_octet, subnet_octet in zip(ip_octets, subnet_octets):
        subnet_bin = bin(int(subnet_octet))[2:].zfill(8)
        ip_bin = bin(int(ip_octet))[2:].zfill(8)
        for subnet_bit, ip_bit in zip(subnet_bin, ip_bin):
            if subnet_bit == '1' and ip_bit == '1':
                prefix += 1
            else:
                break
    return prefix


if __name__ == "__main__":
    ip_address = sys.argv[1]
    subnet_mask = sys.argv[2]
    prefix = calculate_prefix(ip_address, subnet_mask)
    print(prefix)
