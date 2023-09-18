import os
from datetime import datetime
import csv
import re

def format_ip(ip_address):
    """Format IP address to fill missing octets with zeros."""
    return '.'.join([f"{int(octet):03}" for octet in ip_address.split('.')])

def unix_to_human_readable(timestamp):
    """Convert Unix timestamp to human-readable format."""
    dt = datetime.utcfromtimestamp(int(timestamp))
    return dt.strftime('%d.%m.%y / %H:%M:%S')

def import_arp_file(file):
    timestamp = datetime.now().strftime('%y%m%d')
    filename = f'arpwatch_import_{timestamp}.csv'
    file_path = os.path.join('data', 'import', filename)
    
    # Read the uploaded file content
    content = file.read().decode('utf-8')
    
    # Convert content to list of rows
    new_data = [row.split('\\t') for row in content.splitlines()]
    
    # Process new data
    for i, row in enumerate(new_data):
        # Format IP address
        row[1] = format_ip(row[1])
        # Convert Unix timestamp to human-readable format
        row[2] = unix_to_human_readable(row[2])
        # Convert the row to CSV format
        new_data[i] = ';'.join(row) + ';No'  # 'No' is added for the 'Known or Not' field
    
    # Path to the arp_data.csv file
    arp_data_path = os.path.join("data", "arp_data.csv")
    
    # Read existing arp_data.csv
    existing_data = []
    if os.path.exists(arp_data_path):
        with open(arp_data_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            existing_data = list(reader)
    
    # Check and append new entries
    for row in new_data:
        mac_address, ip_address = row.split(';')[0], row.split(';')[1]
        if not any(existing_row[0] == mac_address and existing_row[1] == ip_address for existing_row in existing_data):
            existing_data.append(row.split(';'))
    
    # Write the updated data back to arp_data.csv
    with open(arp_data_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(existing_data)
    
    return True

def import_arpwatch_log(file):
    # Check if file exists
    arp_log_path = os.path.join("data", "arp_log.csv")
    if not os.path.exists(arp_log_path):
        with open(arp_log_path, 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["From", "To", "Subject", "hostname", "ip address", "interface", "ethernet address", "ethernet vendor", "timestamp"])  # Write header

    # Read the uploaded file content
    content = file.read().decode('utf-8')

    # Regular expression pattern to extract fields from ARPwatch log entry
    pattern = re.compile(r"From: (?P<From>.*?) \(.*?\)\nTo: (?P<To>.*?)\nSubject: (?P<Subject>.*?)\n.*?hostname: (?P<hostname>.*?)\n.*?ip address: (?P<ip_address>.*?)\n.*?interface: (?P<interface>.*?)\n.*?ethernet address: (?P<ethernet_address>.*?)\n.*?ethernet vendor: (?P<ethernet_vendor>.*?)\n.*?timestamp: (?P<timestamp>.*?)\n", re.DOTALL)

    # Extract fields using the regular expression pattern
    matches = pattern.findall(content)

    # Convert matches to CSV format
    csv_data = []
    for match in matches:
        # Modify the "Subject" field to remove redundant information
        subject = match[2].split(" (")[0]
        
        # Convert the timestamp to the desired format
        timestamp = datetime.strptime(match[8], "%A, %B %d, %Y %H:%M:%S %z")
        formatted_timestamp = timestamp.strftime("%Y:%m:%d / %H:%M:%S %z")
        
        row = list(match[:2]) + [subject] + list(match[3:8]) + [formatted_timestamp]
        csv_data.append(";".join(row))

    # Read existing arp_log.csv
    existing_data = []
    if os.path.exists(arp_log_path):
        with open(arp_log_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            existing_data = list(reader)

    # Check and append new entries
    for row in csv_data:
        if row not in existing_data:
            existing_data.append(row.split(';'))

    # Write the updated data back to arp_log.csv
    with open(arp_log_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(existing_data)

    return True
