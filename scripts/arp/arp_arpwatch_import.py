import os
from datetime import datetime

def import_arp_file(file):
    timestamp = datetime.now().strftime('%y%m%d')
    filename = f'arpwatch_import_{timestamp}.csv'
    file_path = os.path.join('data', 'import', filename)
    
    # Read the uploaded file content
    content = file.read().decode('utf-8')
    
    # Replace tabs with semicolons
    content = content.replace('\t', ';')
    
    # Save the modified content to the new file
    with open(file_path, 'w') as new_file:
        new_file.write(content)
    
    return True
