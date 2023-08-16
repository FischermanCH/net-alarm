import os
import csv
from datetime import datetime

def get_latest_arp_file():
    files = [f for f in os.listdir('data/import') if f.startswith('arpwatch_import_')]
    files.sort(reverse=True)
    if files:
        return os.path.join('data/import', files[0])
    return None

def update_arp_data(latest_file):
    arp_data_path = 'data/arp_data.csv'
    existing_data = []

    # Load existing arp_data.csv
    if os.path.exists(arp_data_path):
        with open(arp_data_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            existing_data = list(reader)

    # Load latest ARP file
    with open(latest_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        new_data = list(reader)

    # Update existing data with new data
    for row in new_data:
        if row not in existing_data:
            existing_data.append(row)

    # Save updated data back to arp_data.csv
    with open(arp_data_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(existing_data)

    return existing_data

def get_arp_table_data():
    latest_file = get_latest_arp_file()
    if latest_file:
        return update_arp_data(latest_file)
    return []

