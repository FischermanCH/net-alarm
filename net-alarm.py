from flask import Flask, render_template, request, jsonify
import csv
import os
import configparser
from scripts.arp_arpwatch_import import import_arp_file
from scripts.arp_arpwatch_config import save_config_to_file, is_arpwatch_running, run_arpwatch, stop_arpwatch

app = Flask(__name__)

# Default configuration structure
DEFAULT_CONFIG = {
    'Debug': {'Mode': 'False'},
    'File': {'DataFile': ''},
    'Interface': {'Name': ''},
    'Network': {'AdditionalLocalNetworks': ''},
    'Bogon': {'DisableReporting': 'False'},
    'Packet': {'ReadFromFile': ''},
    'Privileges': {'DropRootAndChangeToUser': ''},
    'Email': {'Recipient': '', 'Sender': ''}
}

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
    """Parses the configuration data, ensuring all sections and keys are present."""
    config = configparser.ConfigParser()
    config.read_string(config_data)

    for section, keys in DEFAULT_CONFIG.items():
        if not config.has_section(section):
            config.add_section(section)
        for key, default_value in keys.items():
            if not config.has_option(section, key):
                config.set(section, key, default_value)

    return config

def construct_arpwatch_command(config):
    """Constructs the arpwatch command based on the configuration."""
    command_parts = {
        'Debug': {'Mode': {'on': ' -d'}},
        'File': {'DataFile': ' -f '},
        'Interface': {'Name': ' -i '},
        'Network': {'AdditionalLocalNetworks': ' -n '},
        'Bogon': {'DisableReporting': {'True': ' -N'}},
        'Packet': {'ReadFromFile': ' -r '},
        'Privileges': {'DropRootAndChangeToUser': ' -u '},
        'Email': {'Recipient': ' -m ', 'Sender': ' -s '}
    }

    arpwatch_command = "arpwatch"
    for section, options in command_parts.items():
        for option, value in options.items():
            config_value = config[section][option]
            if isinstance(value, dict):
                arpwatch_command += value.get(config_value, '')
            elif config_value:
                arpwatch_command += value + config_value

    return arpwatch_command

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
            'Bogon': {'DisableReporting': 'True' if request.form.get('disableBogon') else 'False'},
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

    # Controll the arpwatch command
    arpwatch_command = construct_arpwatch_command(config)
    print("Arpwatch Command:", arpwatch_command)  # Debug print
    arpwatch_running = is_arpwatch_running()
    return render_template('arp_arpwatch_config.html', config=config, arpwatch_running=arpwatch_running, arpwatch_command=arpwatch_command)


    arpwatch_command = construct_arpwatch_command(config)
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
    hostname = request.form.get('hostname')
    ip = request.form.get('ip')
    # Code to update the hostname
    return jsonify(message='Hostname updated successfully', category='success')

@app.route('/update_known', methods=['POST'])
def update_known():
    known = request.form.get('known')
    ip = request.form.get('ip')
    # Code to update the known status
    return jsonify(message='Known status updated successfully', category='success')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)