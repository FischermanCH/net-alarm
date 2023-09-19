import os
from flask import render_template, request
import configparser
import subprocess

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
# Handles the rendering of the arpwatch configuration page, processing form data,
# constructing the arpwatch command, determining arpwatch status, and rendering the HTML template.
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
    # Constructing the arpwatch command based on the configuration
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

    arpwatch_running = is_arpwatch_running()  # Determine if arpwatch is running
    return render_template('arp_arpwatch_config.html', config=config, arpwatch_command=arpwatch_command, arpwatch_running=arpwatch_running)

# Parses the arpwatch configuration data, ensuring all sections and keys are present,
# and returns a configuration object.
def parse_config(config_data):
    config = {}
    current_section = None

for line in config_data.splitlines():
    line = line.strip()
    if not line.startswith(('#', '[')) and '=' in line:
        option, value = line.split('=')
        option = option.strip()
        value = value.strip()
            if current_section:
                if current_section not in config:
                    config[current_section] = {}
                config[current_section][option] = value
        elif line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]

    return config

# Checks if arpwatch is currently running on the system by using the 'pgrep' command.
# Returns True if running, False otherwise.
def is_arpwatch_running():
    try:
        result = subprocess.run(['pgrep', 'arpwatch'], stdout=subprocess.PIPE, check=True)
        return bool(result.stdout)
    except subprocess.CalledProcessError:
        return False

# Attempts to stop arpwatch using the 'pkill' command.
# Returns a success message if successful, an error message otherwise.
def stop_arpwatch():
    try:
        subprocess.run(['pkill', 'arpwatch'], check=True)
        return 'Arpwatch stopped successfully.', 'success'
    except subprocess.CalledProcessError:
        return 'Failed to stop arpwatch.', 'error'

# Attempts to start arpwatch using the configuration specified in 'arpwatch.conf'.
# Returns a success message if successful, an error message otherwise.
def run_arpwatch():
    """
    Run arpwatch with the current configuration.
    """
    # Load the current configuration
    with open(CONFIG_FILE_PATH, 'r') as file:
        config_data = file.read()

    config = parse_config(config_data)

    # Construct the arpwatch command from the parsed configuration
    command = config["command"]

    try:
        # Run the arpwatch command
        subprocess.run(command, check=True, shell=True)
        return "Arpwatch started successfully.", "success"
    except subprocess.CalledProcessError:
        return "Error starting arpwatch. Check the configuration and try again.", "danger"

# Saves the provided form data to the specified configuration file path.
# Converts the form data into the appropriate configuration format.
def save_config_to_file(form_data, config_file_path):
    config = configparser.ConfigParser()
    for section, options in form_data.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, str(value))  # Convert value to string
    with open(config_file_path, 'w') as f:
        config.write(f)
