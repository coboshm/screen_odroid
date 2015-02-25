#!/bin/bash

echo "Installing"

echo "Updating system package database..."
sudo apt-get -qq update > /dev/null

echo "Upgrading the system..."
echo "(This might take a while.)"
sudo apt-get -y -qq upgrade > /dev/null

echo "Installing dependencies..."
sudo apt-get -y -qq install python-pip

echo "Installing more dependencies..."
sudo pip install -r ~/screen_odroid/requirements.txt -q
