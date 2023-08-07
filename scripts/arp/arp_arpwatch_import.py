import os
from datetime import datetime

def import_arp_file(file):
    if file.filename.endswith('.csv'):
        timestamp = datetime.now().strftime('%y%m%d')
        filename = f'arpwatch_import_{timestamp}.csv'
        file_path = os.path.join('data', 'import', filename)
        file.save(file_path)
        return True
    return False
