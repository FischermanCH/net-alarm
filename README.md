## Python Application
# Webbased Network Inventory/Alarming based on arpwatch & nmap
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
        - table is sorted by IP on load
        - table / hostname is editable, changes saved on "change focus" to net-alarm/data/arp_data.csv
        - adding column for "known" MAC addresses, clickable "Yes / No" with additional colum entry in net-alarm/data/arp_data.csv
            - still need some adjustement as its only visible if page reload
- CSS file generation to support themes in the future ;-)

---

**Thing's to do :**
GENERIC
- ...
- ...
ARP
- generate arpwatch configure and start page
- replace "edit actual arp-file" with arpwatch-config and use "show actual arp-file" as main arp-show and manipulate page
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

---

File structure 
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