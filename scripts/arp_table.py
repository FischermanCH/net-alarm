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
    pass  # Existing code for updating ARP data

# Function to set up arp_table routes
def setup_arp_table_routes(app):
    # Endpoint to update hostname
    @app.route('/update_hostname', methods=['POST'])
    def update_hostname():
        mac_address = request.form.get('mac_address')
        ip_address = request.form.get('ip_address')
        hostname = request.form.get('hostname')
        known = request.form.get('known')
        print(f"Received data: MAC: {mac_address}, IP: {ip_address}, Hostname: {hostname}, Known: {known}") # Debug print
        update_arp_data(mac_address, ip_address, hostname, known)
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
    print(f"Updating ARP data for MAC: {mac_address}, IP: {ip_address}, Hostname: {hostname}, Known: {known}")
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] == mac_address and row[1] == ip_address:
                if hostname is not None:
                    row[3] = hostname
                if known is not None:
                    row[5] = known
            updated_data.append(row)
    print(f"Updated Data: {updated_data}")
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(updated_data)