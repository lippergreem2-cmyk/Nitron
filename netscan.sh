#!/data/data/com.termux/files/usr/bin/bash

echo "=== Home Network Device Scanner ==="
echo "Scanning your own WiFi network for connected devices..."
echo ""

MY_IP="172.31.203.174"
SUBNET="172.31.203.0/24"

echo "Your device IP: $MY_IP"
echo "Scanning subnet: $SUBNET"
echo ""

nmap -sn "$SUBNET" | grep -E "Nmap scan report|MAC Address"

echo ""
echo "=== Scan complete ==="
echo "Any device listed above is connected to YOUR network."
echo "If you don't recognize a device, change your WiFi password"
echo "and enable WPA3/WPA2 encryption in your router settings."
