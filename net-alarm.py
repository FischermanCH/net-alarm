from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arp')
def arp_page():
    return render_template('arp_page.html')

@app.route('/tcpip')
def tcpip_page():
    return render_template('tcpip_page.html')

@app.route('/host')
def host_page():
    return render_template('host_page.html')

@app.route('/lan')
def lan_page():
    return render_template('lan_page.html')

@app.route('/arp_arpwatch_import')
def arp_arpwatch_import():
    return render_template('arp_arpwatch_import.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
