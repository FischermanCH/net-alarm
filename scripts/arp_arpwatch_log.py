import os

def get_latest_arpwatch_log():
    log_directory = 'data/arpwatch'
    log_files = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))]
    latest_log_file = max(log_files, key=lambda x: os.path.getmtime(os.path.join(log_directory, x)))
    log_file_path = os.path.join(log_directory, latest_log_file)

    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    return ''.join(reversed(log_content))
