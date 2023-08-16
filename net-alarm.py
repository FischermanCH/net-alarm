from flask import Flask, render_template, request
from scripts.arp.arp_arpwatch_import import import_arp_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arp_page')
def arp_page():
    return render_template('arp_page.html')

@app.route('/tcpip_page')
def tcpip_page():
    return render_template('tcpip_page.html')

@app.route('/host_page')
def host_page():
    return render_template('host_page.html')

@app.route('/lan_page')
def lan_page():
    return render_template('lan_page.html')

@app.route('/arp_arpwatch_import', methods=['GET', 'POST'])
def arp_arpwatch_import():
    if request.method == 'POST':
        file = request.files['file']
        if import_arp_file(file):
            return 'ARP Import Script Executed Successfully :-)'
        else:
            return 'Invalid file format. Please upload a valid file.'
    return render_template('arp_arpwatch_import.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
