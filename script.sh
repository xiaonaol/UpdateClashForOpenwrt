#!/bin/bash
opkg update
opkg install python3
opkg install python3-pip
pip install pyinstaller
pyinstaller -F main.py