package main

import (
	"fmt"
	"net"

	"github.com/PaloAltoNetworks/go-panos"
)

func main() {
	// Get the device group name and destination IP address to check
	deviceGroup := "myDeviceGroup"
	destIP := net.ParseIP("10.0.0.1")
	if destIP == nil {
		fmt.Println("Invalid destination IP address")
		return
	}

	// Connect to the Panorama using the API
	client, err := panos.NewClient("panorama.example.com", "admin", "password", true)
	if err != nil {
		panic(err)
	}

	// Get the virtual routers configuration for the specified device group
	vrConfig, err := client.Panorama.DeviceGroup(deviceGroup).VR.Get()
	if err != nil {
		panic(err)
	}

	// Loop through each virtual router
	for _, vr := range vrConfig.VirtualRouters {
		// Loop through each entry in the virtual router
		for _, entry := range vr.StaticRoutes {
			// Check if the destination IP address matches the CIDR of the route
			_, network, err := net.ParseCIDR(entry.Destination)
			if err != nil {
				panic(err)
			}
			if network.Contains(destIP) {
				// If the IP address matches the CIDR, get the next hop IP address
				nextHopIP := net.ParseIP(entry.Nexthop)
				if nextHopIP == nil {
					fmt.Printf("Invalid next hop IP address: %s", entry.Nexthop)
					return
				}
				fmt.Printf("Next hop IP address for %s is %s\n", destIP, nextHopIP)
				return
			}
		}
	}

	fmt.Printf("No matching route found for destination IP address %s in device group %s\n", destIP, deviceGroup)
}
