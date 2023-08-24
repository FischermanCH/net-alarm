import os
import csv
from datetime import datetime
from flask import request, jsonify

# Function to read ARP table data from CSV file
def get_arp_table_data():
    """Reads the arp_data.csv file and returns its content."""
    data = []
    file_path = os.path.join("data", "arp_data.csv")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
    return data

def get_latest_arp_file():
    files = [f for f in os.listdir('data/import') if f.startswith('arpwatch_import_')]
    files.sort(reverse=True)
    if files:
        return os.path.join('data/import', files[0])
    return None

def update_arp_data(latest_file):
    arp_data_path = 'data/arp_data.csv'
    existing_data = []
    existing_entries = set()

    if os.path.exists(arp_data_path):
        with open(arp_data_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                existing_data.append(row)
                existing_entries.add((row[0], row[1]))

    with open(latest_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        new_data = list(reader)

    for row in new_data:
        timestamp = int(row[2])
        formatted_date = datetime.utcfromtimestamp(timestamp).strftime('%d.%m.%y / %H:%M:%S')
        row[2] = formatted_date
        # Pad IP address with zeros for sorting
        ip_parts = row[1].split('.')
        padded_ip = '.'.join(str(int(part)).zfill(3) for part in ip_parts)
        row[1] = padded_ip
        if (row[0], row[1]) not in existing_entries:
            existing_data.append(row)
            existing_entries.add((row[0], row[1]))

    with open(arp_data_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(existing_data)

    return existing_data

# Function to set up arp_table routes
def setup_arp_table_routes(app):
    # Endpoint to update hostname
    @app.route('/update_hostname', methods=['POST'])
    def update_hostname():
        data = request.json
        mac_address = data['macAddress']
        ip_address = data['ipAddress']
        hostname = data['hostname']
        update_arp_data(mac_address, ip_address, hostname=hostname)
        return jsonify(message='Hostname updated successfully', category='success')


# Endpoint to update hostname
@app.route('/update_hostname', methods=['POST'])
def update_hostname():
    data = request.json
    mac_address = data['macAddress']
    ip_address = data['ipAddress']
    hostname = data['hostname']
    update_arp_data(mac_address, ip_address, hostname=hostname)
    return jsonify(message='Hostname updated successfully', category='success')

# Endpoint to update known status
@app.route('/update_known', methods=['POST'])
def update_known():
    data = request.json
    mac_address = data['macAddress']
    ip_address = data['ipAddress']
    known = data['known']
    update_arp_data(mac_address, ip_address, known=known)
    return jsonify(message='Known status updated successfully', category='success')

# Function to update ARP data
def update_arp_data(mac_address, ip_address, hostname=None, known=None):
    file_path = os.path.join("data", "arp_data.csv")
    updated_data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] == mac_address and row[1] == ip_address:
                if hostname is not None:
                    row[3] = hostname
                if known is not None:
                    row[5] = known
            updated_data.append(row)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(updated_data)
