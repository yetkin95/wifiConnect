#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import re
import time

def check_connection_status():
    connection_status = os.system("ping -c 1 8.8.8.8")  
    if connection_status == 0:
        return True
    else:
        return False

def scan_wifi_networks(interface="wlan0", timeout=1.0):
    """Scan Wi-Fi Networks"""
    start_time = time.time()
    all_ssids = []  

    try:
        while True:
            if time.time() - start_time > timeout:
                break

            result = subprocess.check_output(
                ["sudo", "nmcli", "-t", "-f", "SSID", "dev", "wifi"],
                stderr=subprocess.STDOUT
            )
            
            result = result.decode("utf-8")
            ssids = result.splitlines()
            all_ssids.extend(ssids)

    except subprocess.CalledProcessError as e:
        print(f"Error occured while scanning networks: {e}")
    except subprocess.TimeoutExpired:
        print("timeout expired")

    unique_ssids = list(set(all_ssids))  
    print(unique_ssids)
    return unique_ssids

def connect_to_wifi(ssid, password, interface="wlan0"):
    try:
        print(f"Connecting {ssid}...")
        subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)

        result = subprocess.run(["ping", "-c", "3", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print("Success!")
            return 0
        else:
            print("Connection failed. Please check ssid and password")
            print(f"Ping hatası: {result.stderr.decode()}")
            return 1
    except subprocess.CalledProcessError as e:
        print(f"Connectşon Error: {e}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return 1