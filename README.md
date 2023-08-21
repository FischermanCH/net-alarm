## Webbased Network Inventory/Alarming based on arpwatch & nmap
# (by Fischerman.ch and Friend's)

Goal is to create a web-based network inventory/alarming for small/home LAN's.
- NO fancy DB server, all in flattfiles
- Easy and understandable for (skilled) end-user's
- Posibility to work with import-files (to avoid root-issue when running aprwatch or nmap)
- Posibility to export in different formats, (e.g. export a hostfile for your FW/pi-hole)
- Integration and configuration for aprwatch and nmap
- Posibility for some kind of an alerting (if used with integrated arpwatch/nmap)
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

- CSS file generation to support themes in the future ;-)

---

**Thing's to do :**
GENERIC
- think about adding more detection sources as arpwatch alone seenms not to be enough
    - p0f
    - netdiscover
- ...
ARP
- generate arpwatch configure and start page
- ....
- ....

HOST
- ....
- ....

LAN
- ....
- ....

ALERTING
- configure alerting
    - e-mail
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

#### Troubleshooting:
- Port Already in Use: If you see an error that the port 7777 is already in use, you can either:
    - Stop the other service using that port.
Or, 
    - modify the net-alarm.py file to use a different port by changing the line app.run(host='0.0.0.0', port=7777) to a different port number, like port=8888.

#### Missing Dependencies: 
Ensure you've activated the virtual environment and installed all the required packages using pip.

---
## File structure 
```
net-alarm
/home/fischerman/net-alarm/net-alarm
├── data
│   ├── arp_data.csv
│   ├── arpwatch
│   │   ├── arpwatch_2308110108                     no git-sync
│   │   ├── arpwatch_2308110108-                    no git-sync
│   │   ├── arpwatch_output_2308110108.log          no git-sync
│   │   └── testfile.txt
│   ├── export
│   └── import
│       ├── arpwatch_import_230816.csv              no git-sync
│       └── arpwatch_import_230817.csv              no git-sync
├── net-alarm.py
├── README.md
├── scripts
│   ├── arp
│   │   ├── arp_arpwatch_import.py
│   │   ├── arp_table.py
│   │   └── __pycache__
│   │       ├── arp_arpwatch_import.cpython-39.pyc  no git-sync
│   │       └── arp_table.cpython-39.pyc            no git-sync
│   ├── hosts
│   ├── lan
│   └── tcpip
├── static
│   ├── css
│   │   └── styles.css
│   └── images
│       └── icon_placeholder.png
└── templates
    ├── arp_arpwatch_import.html
    ├── arp_page.html
    ├── arp_table.html
    ├── host_page.html
    ├── index.html
    ├── lan_page.html
    └── tcpip_page.html
```