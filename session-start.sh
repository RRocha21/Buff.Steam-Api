#!/bin/bash

# Function to print system information
print_system_info() {
    echo "-----------------------------------------------------------------------------------------------------------------"
    echo "System Information:"
    echo "-----------------------------------------------------------------------------------------------------------------"
    echo "System load: $(uptime | awk -F'[a-z]:' '{print $2}') $(vcgencmd measure_temp | grep -o '[0-9]*\.[0-9]*') C"
    echo "Usage of /: $(df -h / | awk 'NR==2 {print $5}') of $(df -h / | awk 'NR==2 {print $2}')"
    echo "Processes: $(ps aux | wc -l)"
    echo "Memory usage: $(free -m | awk 'NR==2 {print $3/$2 * 100}')%"
    echo "Users logged in: $(who | wc -l)"
    echo "Swap usage: $(free -m | awk 'NR==4 {print $3/$2 * 100}')%"
    echo "IPv4 address for eth0: $(ip addr show eth0 | grep 'inet\b' | awk '{print $2}')"
    echo "-----------------------------------------------------------------------------------------------------------------"
}

# Prompt the user to choose between Script A and Script B
echo "Hello There! I will now start to run the script for you."

# Activate PostgreSQL
echo "Activating PostgreSQL"
sudo systemctl start postgresql.service
echo "PostgreSQL activated"

# Now activate both the Steam-Float-Checker and Buff.Steam-API simultaneously

# Activate the Steam-Float-Checker
echo "Activating Steam-Float-Checker"
cd ../../../../home/rr/git/Steam-Float-Checker/
npm start &

# Activate the Buff.Steam-API
echo "Activating Buff.Steam-API"
cd ../../../../home/rr/git/Buff.Steam-Api/
bash start.sh &

echo "Both scripts have been activated"

# Start printing system information every 60 seconds
while true; do
    print_system_info
    sleep 60
done