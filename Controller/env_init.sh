#!/bin/bash
set -e

echo "Updating package index..."
sudo apt-get update

echo "Installing dependencies..."
sudo apt-get install -y wget apt-transport-https gnupg lsb-release ca-certificates nmap

echo "Adding Aqua Security GPG key..."
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | \
  gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null

echo "Adding Trivy repository..."
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | \
  sudo tee /etc/apt/sources.list.d/trivy.list

echo "Installing Trivy..."
sudo apt-get update
sudo apt-get install -y trivy

echo "Checking versions..."
trivy --version
nmap --version

echo "Installation complete!"
