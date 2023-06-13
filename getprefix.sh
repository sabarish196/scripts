#!/bin/bash

ip_address="192.168.1.100"
subnet_mask="255.255.255.0"

IFS='.' read -r -a ip_octets <<< "$ip_address"
IFS='.' read -r -a subnet_octets <<< "$subnet_mask"

prefix=0
for ((i=0; i<${#subnet_octets[@]}; i++)); do
  subnet_octet=${subnet_octets[i]}
  ip_octet=${ip_octets[i]}
  
  subnet_bin=$(printf "%08d" $(bc <<< "obase=2;$subnet_octet"))
  ip_bin=$(printf "%08d" $(bc <<< "obase=2;$ip_octet"))
  
  for ((j=0; j<8; j++)); do
    subnet_bit=${subnet_bin:j:1}
    ip_bit=${ip_bin:j:1}
    
    if [[ $subnet_bit == "1" && $ip_bit == "1" ]]; then
      prefix=$((prefix+1))
    else
      break
    fi
  done
done

echo "$prefix"
