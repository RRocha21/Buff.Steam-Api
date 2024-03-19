#!/bin/bash

# Prompt the user to choose between Script A and Script B
echo "Hello There! I will now start to run the script for you."


# Activate postgreSQL
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