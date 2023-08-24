import os

def get_latest_arpwatch_logfile():
    log_directory = '/var/log/arpwatch'
    log_files = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))]
    latest_log_file = max(log_files, key=lambda x: os.path.getmtime(os.path.join(log_directory, x)))
    return os.path.join(log_directory, latest_log_file)

def get_latest_arpwatch_log():
    log_file_path = get_latest_arpwatch_logfile()
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()
    log_content.reverse()  # Reverse the order of the log content
    return ''.join(log_content)
