# net-alarm-arp.py

import os
import csv
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this to a strong secret key
app.template_folder = 'web'  # Set the template folder to 'web'
csrf = CSRFProtect(app)

# Path to the CSV file
csv_file_path = os.path.join("data", "net-alarm-arp.csv")

# Rest of the code remains the same

# Check if net-alarm-arp.csv is empty
def is_csv_empty():
    return not os.path.isfile(csv_file_path) or os.stat(csv_file_path).st_size == 0

# Read CSV data into a list of dictionaries
def read_csv_data():
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

# FlaskForm to handle the file upload
class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

# Flask route to handle the ARP file import
@app.route('/', methods=['GET', 'POST'])
def import_arp_data():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():  # Add form validation check
        file = form.file.data
        if file.filename.endswith('.arp'):
            file_path = os.path.join("data", file.filename)
            file.save(file_path)

            if is_valid_arp_file(file_path):
                import_arpwatch_data(file_path)
                os.remove(file_path)
                return "ARP data imported successfully!"
            else:
                os.remove(file_path)
                return "Invalid ARP file format. Please select a valid ARP file with the correct format."
        else:
            return "Please select a file with the .arp extension."

    # Modify the template rendering here
    csv_empty = is_csv_empty()
    csv_data = read_csv_data()
    return render_template('net-alarm-arp.html', form=form, csv_empty=csv_empty, csv_data=csv_data)

if __name__ == '__main__':
    app.run()
