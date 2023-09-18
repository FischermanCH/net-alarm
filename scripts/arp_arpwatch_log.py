import os
import re
import csv


def get_latest_arpwatch_log():
    log_directory = 'data/arpwatch'
    log_files = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f)) and re.match(r'arpwatch_output_\d{10}\.log', f)]
    latest_log_file = max(log_files, key=lambda x: os.path.getmtime(os.path.join(log_directory, x)))
    log_file_path = os.path.join(log_directory, latest_log_file)

    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    return ''.join(reversed(log_content))

def get_arpwatch_log_data():
    arp_log_path = os.path.join("data", "arp_log.csv")
    data = []
    with open(arp_log_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)  # Get the headers
        for row in reader:
            data.append(row)
    return headers, data
