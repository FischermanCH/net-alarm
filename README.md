## Python Application
# Webbased Network Inventory based on arpwatch, nmap and other gpl tools

Goal is to create a web-based network inventory for small/home LAN's.
NO fancy DB server, all in flattfiles, 
- for aprwatch output -> arpwatch-csv 
- for each IP address it's own csv-file
- for each host it's own csv-file

If you are interested and would like to participate, [please drop me a note ->](https://www.fischerman.ch/?page_id=11)

and btw, it's black and green because I like black and green ;-)

─────────────────────────────────────────────────────────

Thing's done : 
- very basic index webpage on port 7777 with links to subpages
- very basic subpages with backlink to main
- very basic arpwatch import page (arp_arpwatch_import.html & arp_arpwatch_import.py)
    - basic import of a file working and saved to data/import/arpwatch_import_YYMMDD

─────────────────────────────────────────────────────────

Thing's to do : 

GENERIC
- ...
- ...

ARP
- generate arpwatch configure and start page
- generate arpwatch import
    - should import default arpwatch file, reformating it as csv with ";" as delimiter and save it as arpwatch_import_YYMMDD.csv in data/import
    - diff with data/arp_addresses.csv and add from data/import/arpwatch_import_YYMMDD.csv (latest version) if data is mmissing in data/arp_addresses.csv add it from data/import/arpwatch_import_YYMMDD.csv

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
```
net-alarm
├── data
│   ├── export
│   └── import
├── net-alarm.py
├── README.md
├── scripts
│   ├── arp
│   │   └── arp_arpwatch_import.py
│   ├── hosts
│   ├── lan
│   └── tcpip
├── static
│   └── images
│       └── icon_placeholder.png
└── templates
    ├── arp_arpwatch_import.html
    ├── arp_page.html
    ├── host_page.html
    ├── index.html
    ├── lan_page.html
    └── tcpip_page.html
```


