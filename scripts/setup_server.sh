#!/bin/bash

# Varta Pravah - SERVER STABILIZATION SCRIPT
echo "🛡️ Starting Memory Optimization..."

# 1. Enable 2GB Swap File (Prevents Crashes)
if [ ! -f /swapfile ]; then
    echo "⚡ Creating 2GB Swap file..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    # Make swap permanent across reboots
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap enabled successfully."
else
    echo "ℹ️ Swap file already exists."
fi

# 2. Optimize System Swappiness (Use RAM first, Swap second)
sudo sysctl vm.swappiness=10
echo "✅ Swappiness set to 10."

# 3. Clean Docker Cache (Free Disk Space)
echo "🧹 Cleaning Docker system..."
docker system prune -f

echo "🚀 Server is now optimized for Varta Pravah LIGHT Mode!"
