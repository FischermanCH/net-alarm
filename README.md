## Python Application
# Webbased Network Inventory based on arpwatch, nmap and other gpl tools

Goal is to create a web-based network inventory for small/home LAN's
NO fancy DB server, all in flattfiles, for each IP address it's own csv-file

If you are interested and would like to participate, [please drop me a note ->](https://www.fischerman.ch/?page_id=11)


Thing's done : 
- very basic index webpage on port 7777 with links to subpages
- generate subpages with backlink to main


Thing's to do : 
GENERIC

ARP
- generate arpwatch configure and start page
- generate arpwatch import (code existing, needs to be integrated)

TCP
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


File structure 

net-alarm/
├── app.py
├── static/
│   └── images/
│       └── icon_placeholder.png
├── templates/
│   ├── index.html
│   ├── arp_page.html
│   ├── tcpip_page.html
│   ├── host_page.html
│   └── lan_page.html
└── venv/ (your virtual environment directory, if used)

