#!/bin/bash
set -e

echo "Syncing files to server..."
python sync.py

echo "Restarting server..."
ssh nate@192.168.1.67 "docker restart LibreChat"

echo "Done!"