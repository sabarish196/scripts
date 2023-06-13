#!/bin/bash

ip_address=$1
subnet_mask=$2

# Calculate the binary representation of the subnet mask
IFS='.' read -ra mask_octets <<< "$subnet_mask"
binary_mask=""
for octet in "${mask_octets[@]}"; do
  binary_octet=$(printf "%08d" $(echo "obase=2;$octet" | bc))
  binary_mask="$binary_mask$binary_octet"
done

# Count the number of consecutive 1s in the binary subnet mask
prefix=0
for ((i = 0; i < ${#binary_mask}; i++)); do
  if [[ ${binary_mask:i:1} == "1" ]]; then
    ((prefix++))
  else
    break
  fi
done

echo "Prefix: $prefix"
