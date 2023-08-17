## Python Application
# Webbased Network Inventory based on arpwatch, nmap and other gpl tools

Goal is to create a web-based network inventory for small/home LAN's.
NO fancy DB server, all in flattfiles, 
- for aprwatch output -> arpwatch-csv 
- for each IP address it's own csv-file
- for each host it's own csv-file

If you are interested and would like to participate, [please drop me a note ->](https://www.fischerman.ch/?page_id=11)

and btw, it's black and green because I like black and green ;-)

---

Thing's done : 
- basic index webpage on port 7777 with links to subpages
- basic subpages with backlink to main
- basic arpwatch import page (arp_arpwatch_import.html & arp_arpwatch_import.py)
    - basic import of a file working and saved to data/import/arpwatch_import_YYMMDD.csv with ";" as delemiter
- basic "arp-table" page
    - if not exist, automatic creation of net-alarm/data/arp_data.csv
    - automatic import of latest : net-alarm/data/arpwatch/arpwatch_YYDDMM file, 
        - compare and import if needed to net-alarm/data/arp_data.csv
    - Present result in sortable table

---

Thing's to do : 

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
├── data
│   ├── arp_data.csv                                /no git sync
│   ├── arpwatch
│   │   ├── arpwatch_2308110108                     /no git sync
│   │   ├── arpwatch_2308110108-                    /no git sync
│   │   ├── arpwatch_output_2308110108.log          /no git sync
│   │   └── testfile.txt
│   ├── export
│   └── import
│       ├── arpwatch_import_230816.csv              /no git sync
│       └── arpwatch_import_230817.csv              /no git sync
├── net-alarm.py
├── README.md
├── scripts
│   ├── arp
│   │   ├── arp_arpwatch_import.py
│   │   ├── arp_table.py
│   │   └── __pycache__                             /no git sync
│   │       ├── arp_arpwatch_import.cpython-39.pyc  /no git sync
│   │       └── arp_table.cpython-39.pyc            /no git sync
│   ├── hosts
│   ├── lan
│   └── tcpip
├── static
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