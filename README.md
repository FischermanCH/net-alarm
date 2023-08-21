# Webbased Network Inventory/Alarming based on arpwatch & other GPL tools
### (by Fischerman.ch and Friend's)
#### this project is realized with support from AI 

Goal is to create a web-based network inventory/alarming for small/home LAN's.
- NO fancy DB server, all in flattfiles
- Easy and understandable for (skilled) end-user's
- Posibility to work with import-files (to avoid root-issue when running aprwatch or similar tools)
- Posibility to export in different formats, (e.g. export a hostfile for your FW/pi-hole)
- Integration and configuration for aprwatch and nmap
- Posibility for some kind of an alerting
- Easy installation, maybe also as pre-configured bundle for cheap hardware (Raspi's)

If you are interested and would like to participate, [please drop me a note ->](https://www.fischerman.ch/?page_id=11)

and btw, it's black and green because I like black and green ;-)

---

**Thing's done :**
- index webpage on port 7777 with links to subpages
- subpages with backlink to main
- import page (arp_arpwatch_import.html & arp_arpwatch_import.py)
    - import of a arpwatch file working and saved to data/import/arpwatch_import_YYMMDD.csv with ";" as delemiter
- "arp-table" page
    - if not exist, automatic creation of net-alarm/data/arp_data.csv
    - automatic import of latest : net-alarm/data/arpwatch/arpwatch_YYDDMM file, 
        - compare and import if needed to net-alarm/data/arp_data.csv
    - present result in sortable table
        - table is sorted by IP on load (featrure lost, due codding)
        - table / hostname is editable, changes saved on "change focus" to net-alarm/data/arp_data.csv
        - adding column for "known" MAC addresses, clickable "Yes / No" with additional colum entry in net-alarm/data/arp_data.csv
            - if "No" is selected, whole row is red
        - all column's are sortable by click on the title
- arpwatch-config page 
    - net-alarm/templates/arp_arpwatch_config.html ; net-alarm/scripts/arp/arp_arpwatch_config.py 
    - form with arpwatch parameter created
    - config file created (net-alarm/static/config/arpwatch.conf)
    - form is writing and reading from config file 

- CSS file generation to support themes in the future ;-)

---

**Thing's to do :**
GENERIC
- think about adding more detection sources as arpwatch alone seenms not to be enough
    - p0f
    - netdiscover
- ...
ARP
- make it possible to start arpwatch from the web interface with the saved configuration
- use the log file for additional information 
    - parse the log-file into a csv
    - show the log file in a table 
    - show the log file in live view 

TCP/IP  -> placeholder, will be replaced when it is clear by what ;-)
HOST    -> placeholder, will be replaced when it is clear by what ;-)
LAN     -> placeholder, will be replaced when it is clear by what ;-)

ALERTING
- configure alerting
    - e-mail
        - e-mail for arpwatch can be configured on /arpwatch/arpwatch Config
    - other 

MAIN PAGE
- Overview for each section
- time and date
- time since last update 

---
## Installation :
### Prerequisites:
```
1.) A system with Python 3.6 or higher installed.
2-) pip (Python package installer) should be installed.
3.) Git installed (for cloning the repository).
4.) arpwatch sourcefile 
```
### Steps:
1.) Clone the Repository:
Open a terminal or command prompt and run:
```
git clone https://github.com/FischermanCH/net-alarm.git
```
2.) Navigate to the Project Directory:
```
cd net-alarm
```
3.) Set Up a Virtual Environment (Optional but Recommended):
It's a good practice to use a virtual environment to avoid potential conflicts with other Python packages.
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
4.) Install Required Packages:
```
pip install Flask
```
5.) Run the Application:
```
python3 net-alarm.py
```
Access the Application:
Open a web browser and navigate to:
```
http://127.0.0.1:7777/
```
or
```
http://SERVER-IP-ADDRESS:7777/
```
### Usage:

- Home Page: Access the main dashboard by navigating to the root URL.
- ARP Page: View and manage ARP data by navigating to /arp_page.
- Import ARP Data: You can import ARP data by navigating to /arp_arpwatch_import and uploading the appropriate ARP data file.
- View ARP Table: To view the ARP table, navigate to /arp_table.
- Generate and save arpwatch configuration

#### Troubleshooting:
- Port Already in Use: If you see an error that the port 7777 is already in use, you can either:
    - Stop the other service using that port.
Or, 
    - modify the net-alarm.py file to use a different port by changing the line app.run(host='0.0.0.0', port=7777) to a different port number, like port=8888.

#### Missing Dependencies: 
Ensure you've activated the virtual environment and installed all the required packages using pip.

---