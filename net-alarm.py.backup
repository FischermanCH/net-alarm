from flask import Flask, render_template, request, jsonify
import csv
import os
# Importing the function from the arp_arpwatch_import script
from scripts.arp.arp_arpwatch_import import import_arp_file
# Importing the function from the arp_arpwatch_config script
from scripts.arp.arp_arpwatch_config import save_config_to_file

app = Flask(__name__)

def get_arp_table_data():
    """Reads the arp_data.csv file and returns its content."""
    data = []
    file_path = os.path.join("data", "arp_data.csv")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arp_page')
def arp_page():
    return render_template('arp_page.html')

@app.route('/arp_arpwatch_config', methods=['GET', 'POST'])
def arp_arpwatch_config():
    if request.method == 'POST':
        form_data = {
            'debug': request.form.get('debug'),
            'file': request.form.get('file'),
            'interface': request.form.get('interface'),
            'network': request.form.get('network'),
            'disableBogon': request.form.get('disableBogon'),
            'readFile': request.form.get('readFile'),
            'dropPrivileges': request.form.get('dropPrivileges'),
            'emailRecipient': request.form.get('emailRecipient'),
            'emailSender': request.form.get('emailSender')
        }
        config_file_path = os.path.join("static", "config", "arpwatch.conf")
        save_config_to_file(form_data, config_file_path)
    return render_template('arp_arpwatch_config.html')

@app.route('/tcpip_page')
def tcpip_page():
    return render_template('tcpip_page.html')

@app.route('/host_page')
def host_page():
    return render_template('host_page.html')

@app.route('/lan_page')
def lan_page():
    return render_template('lan_page.html')

@app.route('/arp_arpwatch_import', methods=['GET', 'POST'])
def arp_arpwatch_import():
    if request.method == 'POST':
        file = request.files['file']
        if import_arp_file(file):
            return 'ARP Import Script Executed Successfully :-)'
        else:
            return 'Invalid file format. Please upload a valid file.'
    return render_template('arp_arpwatch_import.html')

@app.route('/arp_table')
def arp_table():
    arp_data = get_arp_table_data()
    return render_template('arp_table.html', arp_data=arp_data)

@app.route('/update_hostname', methods=['POST'])
def update_hostname():
    data = request.json
    mac_address = data['macAddress']
    ip_address = data['ipAddress']
    new_hostname = data['hostname']

    # Path to the arp_data.csv file
    file_path = os.path.join("data", "arp_data.csv")

    # Read the CSV file and update the hostname
    with open(file_path, 'r') as file:
        rows = list(csv.reader(file, delimiter=';'))

    for row in rows:
        if row[0] == mac_address and row[1] == ip_address:
            row[3] = new_hostname
            break

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return jsonify(success=True)

@app.route('/update_known', methods=['POST'])
def update_known():
    data = request.json
    mac_address = data['macAddress']
    ip_address = data['ipAddress']
    known_value = data['known']

    # Path to the arp_data.csv file
    file_path = os.path.join("data", "arp_data.csv")

    # Read the CSV file and update the known value
    with open(file_path, 'r') as file:
        rows = list(csv.reader(file, delimiter=';'))

    for row in rows:
        if row[0] == mac_address and row[1] == ip_address:
            while len(row) < 6:
                row.append('')
            row[5] = known_value
            break

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
