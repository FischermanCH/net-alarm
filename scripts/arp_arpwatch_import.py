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
    return dt.strftime('%Y.%m.%d %H:%M:%S')

def import_arp_file(file):
    timestamp = datetime.now().strftime('%y%m%d')
    filename = f'arpwatch_import_{timestamp}.csv'
    file_path = os.path.join('data', 'import', filename)
    
    content = file.read().decode('utf-8')
    new_data = [row.split('\t') for row in content.splitlines()]  # Split by tab character
    
    for i, row in enumerate(new_data):
        if len(row) >= 5:
            row[1] = format_ip(row[1])
            row[2] = unix_to_human_readable(row[2])
            new_data[i] = ';'.join(row[:4] + [row[4], 'No'])  # 'No' is added for the 'Known or Not' field
        else:
            return False  # Return False if the row doesn't have the expected data

    arp_data_path = os.path.join("data", "arp_data.csv")
    existing_data = []
    if os.path.exists(arp_data_path):
        with open(arp_data_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            existing_data = list(reader)
    
    for row in new_data:
        mac_address, ip_address = row.split(';')[0], row.split(';')[1]
        if not any(existing_row[0] == mac_address and existing_row[1] == ip_address for existing_row in existing_data):
            existing_data.append(row.split(';'))
    
    with open(arp_data_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(existing_data)
    
    return True


def import_arpwatch_log(file):
    arp_log_path = os.path.join("data", "arp_log.csv")
    if not os.path.exists(arp_log_path):
        with open(arp_log_path, 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["Time/Date:Subject", "MAC Address", "IP Address", "Hostname", "Vendor", "From", "To", "Interface"])

    content = file.read().decode('utf-8')
    pattern = re.compile(r"From: (?P<From>.*?) \(.*?\)\nTo: (?P<To>.*?)\nSubject: (?P<Subject>.*?)\n.*?hostname: (?P<hostname>.*?)\n.*?ip address: (?P<ip_address>.*?)\n.*?interface: (?P<interface>.*?)\n.*?ethernet address: (?P<ethernet_address>.*?)\n.*?ethernet vendor: (?P<ethernet_vendor>.*?)\n.*?timestamp: (?P<timestamp>.*?)\n", re.DOTALL)
    matches = pattern.findall(content)

    csv_data = []
    for match in matches:
        subject = match[2].split(" (")[0]
        timestamp = datetime.strptime(match[8], "%A, %B %d, %Y %H:%M:%S %z")
        formatted_timestamp = timestamp.strftime("%Y.%m.%d %H:%M:%S")
        formatted_ip = format_ip(match[4])
        row = [formatted_timestamp + ":" + subject, match[6], formatted_ip] + list(match[3:6]) + list(match[0:2]) + [match[7]]
        csv_data.append(";".join(row))

    existing_data = []
    if os.path.exists(arp_log_path):
        with open(arp_log_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            existing_data = list(reader)

    for row in csv_data:
        if row not in existing_data:
            existing_data.append(row.split(';'))

    with open(arp_log_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(existing_data)

    return True
