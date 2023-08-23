import os
import csv
from datetime import datetime
from net_alarm import app

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

def get_arp_table_data():
    latest_file = get_latest_arp_file()
    if latest_file:
        return update_arp_data(latest_file)
    return []

@app.route('/update_hostname', methods=['POST'])
def update_hostname():
    hostname = request.form.get('hostname')
    ip = request.form.get('ip')
    # Code to update the hostname
    return jsonify(message='Hostname updated successfully', category='success')
