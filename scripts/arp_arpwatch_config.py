# arp_arpwatch_config.py
import configparser
import subprocess

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
