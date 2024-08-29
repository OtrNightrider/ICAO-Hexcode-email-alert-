#!/usr/bin/env python3

import sys
import os

def is_in_virtual_env():
    # Check for common virtual environment indicators
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        'VIRTUAL_ENV' in os.environ
    )

# Check if we're running in a virtual environment
if is_in_virtual_env():
    print("Running in a virtual environment.")
else:
    print("Not running in a virtual environment.")

# Your existing hexcode.py code starts here:
# For example:
# def main():
#     # Your main function code
#     pass

# if __name__ == "__main__":
#     main()

import socket
import smtplib
from email.mime.text import MIMEText
import time
import sys

# Configuration
HEX_CODE_TO_MONITOR = 'A023F5'
DUMP1090_HOST = '127.0.0.1'
DUMP1090_PORT = 30003  # Standard port for dump1090
EMAIL_TO = 'your_email_here@gmail.com'
EMAIL_FROM = 'your_email_here@gmail.com'
GMAIL_APP_PASSWORD = 'abcd efgh ijkl mnop'  # Ensure this password is correct and secure

def send_email(aircraft_info):
    """Send an email alert when the specified hex code is detected."""
    msg = MIMEText(f"Aircraft with hex code {HEX_CODE_TO_MONITOR} detected:\n{aircraft_info}")
    msg['Subject'] = f'Aircraft Alert: {HEX_CODE_TO_MONITOR}'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_FROM, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_dump1090():
    """Monitor dump1090 for the specified aircraft hex code."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cooldown = False
    
    # Connection retry logic
    for attempt in range(10):  # Try to connect 10 times
        try:
            print(f"Attempting to connect to {DUMP1090_HOST}:{DUMP1090_PORT}...")
            s.connect((DUMP1090_HOST, DUMP1090_PORT))
            print(f"Connected on attempt {attempt + 1}")
            break
        except ConnectionRefusedError:
            print(f"Attempt {attempt + 1} failed. Retrying in 5 seconds...")
            time.sleep(5)
    else:
        print("Failed to connect to dump1090 after multiple attempts.")
        return  # Exit the function if connection fails after all attempts

    while True:
        if cooldown:
            time.sleep(3600)  # Wait for an hour before next alert
            cooldown = False

        data = s.recv(1024).decode('utf-8')
        for line in data.split('\n'):
            if HEX_CODE_TO_MONITOR in line:
                print(f"Detected: {HEX_CODE_TO_MONITOR}")
                send_email(line)
                cooldown = True
                break

if __name__ == "__main__":
    try:
        monitor_dump1090()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
