from flask import Flask, render_template, request, jsonify
import csv
import os
import configparser
from scripts.arp_table import get_arp_table_data, setup_arp_table_routes
from scripts.arp_arpwatch_import import import_arp_file, import_arpwatch_log
from scripts.arp_arpwatch_config import save_config_to_file, is_arpwatch_running, run_arpwatch, stop_arpwatch, DEFAULT_CONFIG, parse_config, arp_arpwatch_config as arp_arpwatch_config_logic
from scripts.arp_arpwatch_log import get_latest_arpwatch_log, get_arpwatch_log_data

app = Flask(__name__)
setup_arp_table_routes(app)

#----------------------------------------------
# Route for the main index page
@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------
# CHAPTER aprwatch
# Route for the ARP page
@app.route('/arp_page')
def arp_page():
    return render_template('arp_page.html')
# - - - - - - - - - - - - - - - - - - - - - - -
# Route for ARP table
@app.route('/arp_table')
def arp_table():
    arp_data = get_arp_table_data()
    return render_template('arp_table.html', arp_data=arp_data)  
# - - - - - - - - - - - - - - - - - - - - - - -
# Route for the ARPwatch configuration page
@app.route('/arp_arpwatch_config', methods=['GET', 'POST'])
def arp_arpwatch_config():
    return arp_arpwatch_config_logic()
# - - - - - - - - - - - - - - - - - - - - - - -
    # Control the arpwatch command
    arpwatch_command = construct_arpwatch_command(config)
    arpwatch_running = is_arpwatch_running()
    return render_template('arp_arpwatch_config.html', config=config, arpwatch_running=arpwatch_running, arpwatch_command=arpwatch_command)
# - - - - - - - - - - - - - - - - - - - - - - -
# Route for arpwatch import
@app.route('/arp_arpwatch_import', methods=['GET', 'POST'])
def arp_arpwatch_import():
    if request.method == 'POST':
        file = request.files['file']
        if import_arp_file(file):
            return 'arpwatch Import Script Executed Successfully :-)'
        else:
            return 'Invalid file format. Please upload a valid file.'
    return render_template('arp_arpwatch_import.html')
# - - - - - - - - - - - - - - - - - - - - - - -
# Route for arpwatch LOG import
@app.route('/arp_arpwatch_log_import', methods=['GET', 'POST'])
def arp_arpwatch_log_import():
    if request.method == 'POST':
        file = request.files['log_file']
        if import_arpwatch_log(file):
            return 'arpwatch Log Import Script Executed Successfully :-)'
        else:
            return 'Invalid file format. Please upload a valid log file.'
    return render_template('arp_arpwatch_log_import.html')
# - - - - - - - - - - - - - - - - - - - - - - -
# Route to run arpwatch
@app.route('/run_arpwatch', methods=['POST'])
def run_arpwatch_route():
    message, category = run_arpwatch()
    return jsonify(message=message, category=category)
# - - - - - - - - - - - - - - - - - - - - - - -
# Route to stop arpwatch
@app.route('/stop_arpwatch', methods=['POST'])
def stop_arpwatch_route():
    message, category = stop_arpwatch()
    return jsonify(message=message, category=category)
#----------------------------------------------
# Route to show arpwatch logfile
@app.route('/arp_arpwatch_log')
def arp_arpwatch_log():
    log_content = get_latest_arpwatch_log()
    headers, data = get_arpwatch_log_data()
    return render_template('arp_arpwatch_log.html', log_content=log_content, headers=headers, data=data)
#----------------------------------------------
# CHAPTER TCPIP
# Route for the TCPIP page
@app.route('/tcpip_page')
def tcpip_page():
    return render_template('tcpip_page.html')
#----------------------------------------------
# CHAPTER host
# Route for the host page
@app.route('/host_page')
def host_page():
    return render_template('host_page.html')
#----------------------------------------------
# CHAPTER LAN
# Route for the LAN page
@app.route('/lan_page')
def lan_page():
    return render_template('lan_page.html')
#----------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
