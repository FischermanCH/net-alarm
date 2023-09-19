import os
from flask import render_template, request
import configparser
import subprocess

# Default configuration structure
DEFAULT_CONFIG = {
    'Debug': {'mode': 'False'},
    'File': {'datafile': ''},
    'Interface': {'name': ''},
    'Network': {'additionallocalnetworks': ''},
    'Bogon': {'disablereporting': 'False'},
    'Packet': {'readfromfile': ''},
    'Privileges': {'droprootandchangetouser': ''},
    'Email': {'recipient': '', 'sender': ''}
}
# Handles the rendering of the arpwatch configuration page, processing form data,
# constructing the arpwatch command, determining arpwatch status, and rendering the HTML template.
def arp_arpwatch_config():
    config_file_path = os.path.join("static", "config", "arpwatch.conf")
    if request.method == 'POST':
        form_data = {
            'Debug': {'mode': request.form.get('debug')},
            'File': {'datafile': request.form.get('file')},
            'Interface': {'name': request.form.get('interface')},
            'Network': {'additionallocalnetworks': request.form.get('network')},
            'Bogon': {'disablereporting': 'True' if request.form.get('disableBogon') else 'False'},
            'Packet': {'readfromfile': request.form.get('readFile')},
            'Privileges': {'droprootandchangetouser': request.form.get('dropPrivileges')},
            'Email': {'recipient': request.form.get('emailrecipient'), 'sender': request.form.get('emailsender')}
        }
        save_config_to_file(form_data, config_file_path)
        config = form_data
    else:
        with open(config_file_path, 'r') as f:
            config_data = f.read()
        config = parse_config(config_data)
    # Constructing the arpwatch command based on the configuration
    command_parts = {
        'Debug': {'mode': {'on': ' -d'}},
        'File': {'datafile': ' -f '},
        'Interface': {'name': ' -i '},
        'Network': {'additionallocalnetworks': ' -n '},
        'Bogon': {'disablereporting': {'True': ' -N'}},
        'Packet': {'readfromfile': ' -r '},
        'Privileges': {'droprootandchangetouser': ' -u '},
        'Email': {'recipient': ' -m ', 'sender': ' -s '}
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
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            config[current_section] = {}
        elif '=' in line and not line.startswith('#'):
            option, value = line.split('=')
            option = option.strip()
            value = value.strip()
            if current_section:
                config[current_section][option] = value
            else:
                config[option] = value
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
        
def load_config_from_file(config_file_path):
    """
    Loads the configuration from the specified file path and returns it as a dictionary.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    config_data = {}
    for section in config.sections():
        config_data[section] = {}
        for option in config.options(section):
            config_data[section][option] = config.get(section, option)
    
    return config_data
