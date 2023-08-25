import os
from datetime import datetime
import csv

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

    # Process content and convert to CSV format
    entries = content.split("\n\n")
    new_data = []
    for entry in entries:
        lines = entry.split("\n")
        split_line = lines[0].split(": ")
        if len(split_line) > 1:
            from_field = split_line[1]
        else:
            # Behandlung des Falls, dass ": " nicht in der Zeile gefunden wurde
            continue  # Zum Beispiel können Sie die Verarbeitung dieses Eintrags überspringen
            to_field = lines[1].split(": ")[1]
            subject_field = lines[2].split(": ")[1]
            details = {line.split(": ")[0].strip(): line.split(": ")[1].strip() for line in lines[3:]}
            details["From"] = from_field
            details["To"] = to_field
            details["Subject"] = subject_field
            new_data.append(details)

    # Convert to CSV format
    csv_data = []
    for entry in new_data:
        row = [
            entry["From"],
            entry["To"],
            entry["Subject"],
            entry["hostname"],
            entry["ip address"],
            entry["interface"],
            entry["ethernet address"],
            '"' + entry["ethernet vendor"] + '"',
            '"' + entry["timestamp"] + '"'
        ]
        csv_data.append(";".join(row))

    # Read existing arp_log.csv
    existing_data = []
    if os.path.exists(arp_log_path):
        with open(arp_log_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            existing_data = list(reader)

    # Check and append new entries
    for row in csv_data:
        hostname, ip_address, ethernet_address, timestamp = row.split(';')[3], row.split(';')[4], row.split(';')[6], row.split(';')[8]
        if not any(existing_row[3] == hostname and existing_row[4] == ip_address and existing_row[6] == ethernet_address and existing_row[8] == timestamp for existing_row in existing_data):
            existing_data.append(row.split(';'))

    # Write the updated data back to arp_log.csv
    with open(arp_log_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(existing_data)

    return True  # Correctly placed inside the function

