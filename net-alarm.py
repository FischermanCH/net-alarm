from flask import Flask, render_template, request, jsonify
import csv
import os
import configparser
# Importing the function from the arp_arpwatch_import script
from scripts.arp_arpwatch_import import import_arp_file
# Importing the functions from the arp_arpwatch_config script
from scripts.arp_arpwatch_config import save_config_to_file, is_arpwatch_running, run_arpwatch, stop_arpwatch

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

def parse_config(config_data):
    config = configparser.ConfigParser()
    config.read_string(config_data)
    
    # Ensure all sections and keys are present
    default_config = {
        'Debug': {'Mode': 'False'},
        'File': {'DataFile': ''},
        'Interface': {'Name': ''},
        'Network': {'AdditionalLocalNetworks': ''},
        'Bogon': {'DisableReporting': 'False'},
        'Packet': {'ReadFromFile': ''},
        'Privileges': {'DropRootAndChangeToUser': ''},
        'Email': {'Recipient': '', 'Sender': ''}
    }
    
    for section, keys in default_config.items():
        if not config.has_section(section):
            config.add_section(section)
        for key, default_value in keys.items():
            if not config.has_option(section, key):
                config.set(section, key, default_value)
    
    return config

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arp_page')
def arp_page():
    return render_template('arp_page.html')

@app.route('/arp_arpwatch_config', methods=['GET', 'POST'])
def arp_arpwatch_config():
    config_file_path = os.path.join("static", "config", "arpwatch.conf")
    if request.method == 'POST':
        form_data = {
            'Debug': {'Mode': request.form.get('debug')},
            'File': {'DataFile': request.form.get('file')},
            'Interface': {'Name': request.form.get('interface')},
            'Network': {'AdditionalLocalNetworks': request.form.get('network')},
            'Bogon': {'DisableReporting': request.form.get('disableBogon')},
            'Packet': {'ReadFromFile': request.form.get('readFile')},
            'Privileges': {'DropRootAndChangeToUser': request.form.get('dropPrivileges')},
            'Email': {'Recipient': request.form.get('emailRecipient'), 'Sender': request.form.get('emailSender')}
        }
        save_config_to_file(form_data, config_file_path)
        config = form_data
    else:
        with open(config_file_path, 'r') as f:
            config_data = f.read()
        config = parse_config(config_data)

    # Construct the arpwatch command based on the config file
    arpwatch_command = "arpwatch"
    if config['Debug']['Mode'].lower() == 'on':
        arpwatch_command += " -d"
    if config['File']['DataFile']:
        arpwatch_command += " -f " + config['File']['DataFile']
    if config['Interface']['Name']:
        arpwatch_command += " -i " + config['Interface']['Name']
    if config['Network']['AdditionalLocalNetworks']:
        arpwatch_command += " -n " + config['Network']['AdditionalLocalNetworks']
    if config['Bogon']['DisableReporting'] == 'True':
        arpwatch_command += " -N"
    if config['Packet']['ReadFromFile']:
        arpwatch_command += " -r " + config['Packet']['ReadFromFile']
    if config['Privileges']['DropRootAndChangeToUser']:
        arpwatch_command += " -u " + config['Privileges']['DropRootAndChangeToUser']
    if config['Email']['Recipient']:
        arpwatch_command += " -m " + config['Email']['Recipient']
    if config['Email']['Sender']:
        arpwatch_command += " -s " + config['Email']['Sender']

    # Check if arpwatch is running
    arpwatch_running = is_arpwatch_running()
    return render_template('arp_arpwatch_config.html', config=config, arpwatch_running=arpwatch_running)
    
    # Check if arpwatch is running
    arpwatch_running = is_arpwatch_running()
    return render_template('arp_arpwatch_config.html', config=config, arpwatch_running=arpwatch_running)

@app.route('/run_arpwatch', methods=['POST'])
def run_arpwatch_route():
    message, category = run_arpwatch()
    return jsonify(message=message, category=category)

@app.route('/stop_arpwatch', methods=['POST'])
def stop_arpwatch_route():
    message, category = stop_arpwatch()
    return jsonify(message=message, category=category)


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
    known = data['known']

    # Path to the arp_data.csv file
    file_path = os.path.join("data", "arp_data.csv")

    # Read the CSV file and update the known status
    with open(file_path, 'r') as file:
        rows = list(csv.reader(file, delimiter=';'))

    for row in rows:
        if row[0] == mac_address and row[1] == ip_address:
            row[4] = known
            break

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
