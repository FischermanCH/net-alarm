# arp_arpwatch_config.py
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

# Function to parse the configuration data
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

# Function to construct the arpwatch command
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

def is_arpwatch_running():
    try:
        result = subprocess.run(['pgrep', 'arpwatch'], stdout=subprocess.PIPE, check=True)
        return bool(result.stdout)
    except subprocess.CalledProcessError:
        return False

def stop_arpwatch():
    try:
        subprocess.run(['pkill', 'arpwatch'], check=True)
        return 'Arpwatch stopped successfully.', 'success'
    except subprocess.CalledProcessError:
        return 'Failed to stop arpwatch.', 'error'

def run_arpwatch():
    config_path = 'static/config/arpwatch.conf'
    config = configparser.ConfigParser()
    config.read(config_path)
    user = config['Privileges']['DropRootAndChangeToUser']
    command = ['arpwatch', '-f', config_path, '-U', user]
    
    try:
        subprocess.run(command, check=True)
        return 'Arpwatch started successfully.', 'success'
    except subprocess.CalledProcessError:
        return 'Failed to start arpwatch.', 'error'

def save_config_to_file(form_data, config_file_path):
    config = configparser.ConfigParser()
    for section, options in form_data.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, str(value))  # Convert value to string

    with open(config_file_path, 'w') as f:
        config.write(f)
