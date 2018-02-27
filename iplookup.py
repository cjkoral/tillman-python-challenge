import pandas as pd
import numpy as np
import re
import urllib
import json
import csv
import pprint

ip_list = []
geo_url = "http://freegeoip.net/json/"
rdap_url = "http://rdap.apnic.net/ip/"

def parsefile(textfile):
    with open(textfile, "r") as txt:
        content = txt.read()
        ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", content)
        for i in ips:
            ip_list.append(i)
    with open('IP_List.csv', 'wb') as csvfile:
        geo_write = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        geo_write.writerow(ip_list)
    print textfile+" has been parsed into file and array"

def geoIP_search(string):
    result = []
    res = urllib.urlopen(geo_url+string)
    data = json.loads(res.read())
    ip = data['ip']
    country = data['country_code']
    region = data['region_code']
    regname = data['region_name']
    zipc = data['zip_code']
    longi = str(data['longitude'])
    lati = str(data['latitude'])
    result.append(ip.encode('utf-8'))
    result.append(country.encode('utf-8'))
    result.append(region.encode('utf-8'))
    result.append(regname.encode('utf-8'))
    result.append(zipc.encode('utf-8'))
    result.append(longi.encode('utf-8'))
    result.append(lati.encode('utf-8'))
    name = raw_input("input csv file name: ")
    with open(name+'.csv', 'wb') as csvfile:
        geo_write = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        geo_write.writerow(result)
    with open(name+'.csv', 'rb') as csvfile:
        geo_reader = csv.reader(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for i in geo_reader:
            data = np.array([i])
            df = pd.DataFrame(data, columns=["ip","country","region","area","zip","longitude","latitude"])
    print df+"\n"

def geoIP_all(array):
    geo_list = []
    for i in array:
        result = []
        res = urllib.urlopen(geo_url+i)
        data = json.loads(res.read())
        ip = data['ip']
        country = data['country_code']
        region = data['region_code']
        regname = data['region_name']
        zipc = data['zip_code']
        longi = str(data['longitude'])
        lati = str(data['latitude'])
        result.append(ip.encode('utf-8'))
        result.append(country.encode('utf-8'))
        result.append(region.encode('utf-8'))
        result.append(regname.encode('utf-8'))
        result.append(zipc.encode('utf-8'))
        result.append(longi.encode('utf-8'))
        result.append(lati.encode('utf-8'))
        geo_list.append(result)
    with open('geoIPAll.csv', 'wb') as csvfile:
        geo_write = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        geo_write.writerow(geo_list)
    with open('geoIPAll.csv', 'rb') as csvfile:
        geo_reader = csv.reader(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for i in geo_reader:
            data = np.array(i)
            df = pd.DataFrame(geo_list, columns=["ip","country","region","area","zip","longitude","latitude"])
    print df+"\n"

def rdap_search(string):
    res = urllib.urlopen(rdap_url+string)
    data = json.loads(res.read())
    #ip
    try:
        nhandle = (data['handle']).encode('utf-8')
    except (KeyError, IndexError):
        nhandle = ''
    try:
        startip = (data['startAddress']).encode('utf-8')
    except (KeyError, IndexError):
        startip = ''
    try:
        endip = (data['endAddress']).encode('utf-8')
    except (KeyError, IndexError):
        endip = ''
    try:
        ipv = (data['ipVersion']).encode('utf-8')
    except (KeyError, IndexError):
        ipv = ''
    try:
        phandle = (data['parentHandle']).encode('utf-8')
    except (KeyError, IndexError):
        phandle = ''
    try:
        update = (data['events'][0]['eventDate']).encode('utf-8')
    except (KeyError, IndexError):
        update = ''
    #entity
    try:
        ename = (data['entities'][0]['handle']).encode('utf-8')
    except (KeyError, IndexError):
        ename = ''
    try:
        name = (data['name']).encode('utf-8')
    except (KeyError, IndexError):
        name = ''
    try:
        erole1 = (data['entities'][0]['roles'][0])
    except (KeyError, IndexError):
        erole1 = ''
    try:
        erole2 = (data['entities'][1]['roles'][0])
    except (KeyError, IndexError):
        erole2 = ''
    try:
        ref = (data['links'][1]['href']).encode('utf-8')
    except (KeyError, IndexError):
        ref = ''
    name = raw_input("input csv file name")
    ipform = "IP data"+"\nHandle: "+nhandle+"\nParent Handle: "+phandle+"\nNet range: "+startip+" - "+endip+"\nIP Version: "+ipv+"\nLast Changed: "+update
    entform = "\nEntity"+"\nHandle: "+ename+"\nName: "+name+"\nRole: "+erole1+", "+erole2
    startend = "----------------------------------------------------------------"
    form = "RDAP:"+"\n"+ipform+"\n"+entform+"\n"+"Reference: "+ref+"\n"+startend+"\n"
    print form
    with open(name+'.csv', 'wb') as csvfile:
        geo_write = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        geo_write.writerow(form)

def rdap_all(array):
    rdap = []
    for i in array:
        try:
            res = urllib.urlopen("http://rdap.apnic.net/ip/"+i)
            data = json.loads(res.read())
        except (ValueError):
            val = "error"
        try:
            nhandle = (data['handle']).encode('utf-8')
        except (KeyError, IndexError):
            nhandle = ''
        try:
            startip = (data['startAddress']).encode('utf-8')
        except (KeyError, IndexError):
            startip = ''
        try:
            endip = (data['endAddress']).encode('utf-8')
        except (KeyError, IndexError):
            endip = ''
        try:
            ipv = (data['ipVersion']).encode('utf-8')
        except (KeyError, IndexError):
            ipv = ''
        try:
            phandle = (data['parentHandle']).encode('utf-8')
        except (KeyError, IndexError):
            phandle = ''
        try:
            update = (data['events'][0]['eventDate']).encode('utf-8')
        except (KeyError, IndexError):
            update = ''
        #entity
        try:
            ename = (data['entities'][0]['handle']).encode('utf-8')
        except (KeyError, IndexError):
            ename = ''
        try:
            name = (data['name']).encode('utf-8')
        except (KeyError, IndexError):
            name = ''
        try:
            erole1 = (data['entities'][0]['roles'][0])
        except (KeyError, IndexError):
            erole1 = ''
        try:
            erole2 = (data['entities'][1]['roles'][0])
        except (KeyError, IndexError):
            erole2 = ''
        try:
            ref = (data['links'][1]['href']).encode('utf-8')
        except (KeyError, IndexError):
            ref = ''
        ipform = "IP data"+"\nHandle: "+nhandle+"\nParent Handle: "+phandle+"\nNet range: "+startip+" - "+endip+"\nIP Version: "+ipv+"\nLast Changed: "+update
        entform = "\nEntity"+"\nHandle: "+ename+"\nName: "+name+"\nRole: "+erole1+", "+erole2
        startend = "----------------------------------------------------------------"
        form = "RDAP:"+"\n"+ipform+"\n"+entform+"\n"+"Reference: "+ref+"\n"+startend+"\n"
        print form
        rdap.append(form)
    with open('RDAPAll.csv', 'wb') as csvfile:
        geo_write = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        geo_write.writerow(rdap)
    print "RDAP look up complete! RDAPAll.cvs created"



#main
tfile = raw_input("Input txt file: ")
parsefile(tfile)
#menu
menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"+"\n(5) Exit"
print menuop
menu = raw_input("Input menu option: ")
if (menu == "1"):
    geoIP_all(ip_list)
    menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"+"\n(5) Exit"
    print menuop
    menu = raw_input("Input menu option: ")
if (menu == "2"):
    iplook = raw_input("Input Ip from file for geo look up: ")
    geoIP_search(iplook)
    menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"+"\n(5) Exit"
    print menuop
    menu = raw_input("Input menu option: ")
if (menu == "3"):
    rdap_all(ip_list)
    menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"+"\n(5) Exit"
    print menuop
    menu = raw_input("Input menu option: ")
if (menu == "4"):
    rdap_look = raw_input("Input ip from file for RDAP look up: ")
    rdap_search(rdap_look)
    menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"+"\n(5) Exit"
    print menuop
if (menu == "5"):
    quit()
else:
    menuop = "(1) Geo IP look up of all ip addresses in file"+"\n(2) Geo IP look up of specific ip addres in file"+"\n(3) RDAP look up for all ip addresses in file"+"\n(4) RDAP look up for specific ip addres in file"
    print menuop
    menu = raw_input("Input menu option: ")
