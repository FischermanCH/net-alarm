import glob
import os

def get_latest_arpwatch_log():
    log_file_path = get_latest_arpwatch_logfile()
    log_content = []
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()
    log_content.reverse()  # Reverse the order of the lines
    return ''.join(log_content)
