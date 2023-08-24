import glob
import os

def get_latest_arpwatch_log():
    log_dir = 'data/arpwatch/'
    log_files = glob.glob(os.path.join(log_dir, 'arpwatch_output_*.log'))
    latest_log_file = max(log_files, key=os.path.getctime)
    with open(latest_log_file, 'r') as file:
        log_content = file.read()
    return log_content
