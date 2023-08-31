import socket
import time
import nmap3
# FTP
from ftplib import FTP
# Telnet
import telnetlib
# SMB
from impacket.smbconnection import SMBConnection
from impacket.examples.smbclient import MiniImpacketShell
# Redis
import redis
# Mysql
import mysql.connector
from mysql.connector import Error
# Waf detection
from deps.WafDetector import *
# Dirscan
import wfuzz
import os
# Basic scan
import ipaddress
import whois
from deps.DNSHelper import *
from deps.GeoLocation import *

FTP_PORT = 21
TELNET_PORT = 23
SMB_PORT = 445
REDIS_PORT = 6379
MYSQL_PORT = 3306

NOT_IMPLEMENTED = "[!] Not implemented yet"

PORT_PROMTS = {
    FTP_PORT : "[&] -> Use test_ftp(target, cmds=ftp_cmds) for checking. ftp_cmds can be [\"LIST\", \"PWD\"]",
    TELNET_PORT : "[&] -> Use test_telnet(target, cmds=telnet_cmds) for checking. telnet_cmds can be [\"ls\"]",
    SMB_PORT : "[&] -> Use test_smb(target) for checking",
    REDIS_PORT : "[&] -> Use test_redis(target) for checking",
    MYSQL_PORT : "[&] -> Use test_mysql(target, port, username, password, dbs, limit)",
    80 : "[&] -> Configure scope with web_scan",
    443 : "[&] -> Configure scope with web_scan",
}

DELIMITER = "[+] -----------------------------------------------------------------------------------------------------------------------------"

def to_ip(target):
    if "http" in target:
        target = target.split("://")[1]
    return socket.gethostbyname(target)

def test_ftp(target, port=FTP_PORT, cmds = ["LIST", "PWD"]):
    try:
        print("[*] Testing ftp... ")
        ftp = FTP(target) 
        ftp.login()
        for cmd in cmds:
            print(f"[*] Executing command {cmd}")
            ftp.retrlines(cmd)
        ftp.close()
        print("[*] Close ftp connection... ")
    except IOError as ex:
        print(f"[!] Exception: {ex.strerror} with code {ex.errno}")

def test_telnet(target, port=TELNET_PORT, cmds = ["ls", "exit"]):
    try:
        print("[*] Testing telnet... ")
        username = "root"
        tn = telnetlib.Telnet(target, port)
        print(tn.read_until(b"login: ").decode('utf-8'))
        tn.write(b"root\n")
        time.sleep(5)
        print(tn.read_very_eager().decode('utf-8'))
        
        for cmd in cmds:
            print(f"[*] Executing command {cmd}")
            tn.write(cmd.encode('utf-8') + b"\n")
            time.sleep(2)
            print(tn.read_very_eager().decode('utf-8'))
        tn.close()
        print("[*] Close telnet connection... ")

    except Exception as ex:
        print(f"[!] Exception: {str(ex)}")

def test_smb(target, port=SMB_PORT, cmds = []):
    try:
        print("[*] Testing SMB... ")
        client = SMBConnection(target, target)
        status = client.login("root", "")
        
        if status:
            print(f"[*] Connection to {target} complete")
            resp = client.listShares()
            print(f"[*] Available shares:")
            for i in range(len(resp)):
                share = resp[i]['shi1_netname'][:-1]
                print(f"[*] -> [{share}]")
                try:
                    for line in client.listPath(share, "*"):
                        print(f"[*] --> {line.get_longname()}")
                except Exception as ex:
                    print("[!] Exception: {}".format(ex))
        print("[*] Close SMB connection... ")

    except Exception as ex:
        print(f"[!] Exception: {str(ex)}")

def test_redis(target, port=REDIS_PORT):
    try:
        print("[*] Testing redis... ")
        r = redis.Redis(host=target, port=port, db=0)
        info = r.execute_command("info", "all")
        keys = r.execute_command("keys", "*")
        print("[*] Close redis connection... ")

    except Exception as ex:
        print(f"[!] Exception: {str(ex)}")

def test_mysql(target, port=MYSQL_PORT, username="root", password="", dbs="", limit=10):
    connection = None
    print_samples = True
    dbs_for_skip = ["information_schema", "mysql", "performance_schema"]
    row_limit = 10
    
    try:
        connection = mysql.connector.connect(host=target,
                                             database='',
                                             user='root',
                                             password='')
        if connection.is_connected():
            info = connection.get_server_info()
            print(f"[*] Connected to MySQL Server: {info}")
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")
            print("[*] Databases:")
            dbs = cursor.fetchall()
            for db in dbs:
                print(f"[*] -> Database \"{db[0]}\": ")
                if db[0] in dbs_for_skip:
                    print(f"[!] --> Skip current db as its system db.")
                    continue
                if print_samples:
                    cursor.execute(f"USE {db[0]};")
                    cursor.execute("SHOW TABLES;")
                    tables = cursor.fetchall()
                    for t in tables:
                        print(f"[*] --> Table \"{t[0]}\" sample:")
                        cursor.execute(f"SELECT * FROM {t[0]} LIMIT {row_limit};")
                        rows = cursor.fetchall()
                        for r in rows:
                            print(f"[*] ---> {r};")
        else:
            print("[!] Unable to connect to MySQL :(")
    except Error as e:
        print(f"[!] Error while connecting to MySQL {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("[*] MySQL connection is closed.")

def test_waf(target):
    pass

def nmap_osmatch(target, iface = ""):
    nmap = nmap3.Nmap()
    args = ""
    if iface:
        args = "-e " + iface
    os_results = nmap.nmap_os_detection(target, args = args)
    print(os_results)
    
def nmap_ports(target, top = 100, iface = "", custom = ""):
    nmap = nmap3.Nmap()
    args = ""
    if iface:
        args = "-e " + iface + " "
    if custom:
        args = custom + " "
    ports_ids = []
    try:
        ports = nmap.scan_top_ports(target, top, args = args)[target]
        # TODO: print cmd and create link with https://explainshell.com/explain?cmd=
        # print(ports)
        ports = ports["ports"]
        if isinstance(ports, list):
            print(f"[*] Found {len(ports)} port(s):")
            for p in ports:
                keys = ["name", "product", "version"]
                data = {}
                for k in keys:
                    data[k] = "N/A" if k not in p['service'].keys() else p['service'][k]
                print(f"[*] -> {p['portid']}/{p['protocol']} {p['state']}, service {data['name']}({data['product']}/{data['version']})")
                # Processing 'scripts; if available
                if "scripts" in p and isinstance(p["scripts"], list):
                    for s in p["scripts"]:
                         print(f"[*] --> {s['name']}: {s['raw']}")
                ports_ids.append(int(p['portid']))
    except Exception as ex:
        print("[!] Exception: {}".format(ex))

    return ports_ids

def port_scan(config):
    print("[*] Processing ports...")
    subcfg = config["port_scan"]
    target_ip = to_ip(config["target"])
    for o in subcfg["options"]:
        port_nums = nmap_ports(target_ip, 
                               top=subcfg["top"], 
                               iface=config["iface"], 
                               custom=o)
        for p in port_nums:
            if p in PORT_PROMTS.keys():
                print(PORT_PROMTS[p])
    print("[*] Finished scanning ports.")

def dirs(target, config):
    results = []
    path = "assets/wordlists/"
    wls = config["wordlists"]
    ext_payload = ("list", {"values": "-".join(config["ext"])})

    session = wfuzz.FuzzSession(url=target + "/FUZZ.FUZ2Z")
    for wl in wls:
        file = path + wl
        if not os.path.exists(file):
            print(f"[!] Cant find wordlist {file}")
            continue
        print(f"[*] Processing wordlist {file}...")
        for r in session.fuzz(hc=config["skip_codes"], 
                              payloads=[("file", {"fn": file}),
                                        ext_payload],
                             concurrent=10):
            code = r.code
            entity = r.description.replace(" - ", ".")
            link = target + "/" + entity
            print(f"[*] -> [{code}] Found \"{entity}\": {link}")

def basic_host_scan(config):
    target = config["target"]
    subconf = config["basic_scan"]
    allowed = subconf["subscans"]
    target_ip = to_ip(target)
    private = ipaddress.ip_address(target_ip).is_private

    print(f"[*] Start basic scan for target {target}...")
    if not private:
        print(f"[*] {target}({target_ip}) is public network. Check more: https://ipinfo.io/{target_ip}")
        if "geo" in allowed:
            # Geolocation - {'cc': 'DE', 'country': 'Germany', 'city': 'Frankfurt am Main', 'lat': 50.1109, 'lon': 8.68213, 'region': 'Hesse'}
            g = GeoLocation(subconf["geodb"])
            location = g.get(target_ip)
            lat = location["lat"]
            lon = location["lon"]
            link = f"https://maps.google.com/?q={lat},{lon}"
            address = f"{location['country']}({location['cc']}), {location['region']}, {location['city']}"
            print(f"[*] Geo is {address}. Check {link}")
        if "whois" in allowed:
            # Whois
            w = whois.whois(target)
            print("[*] Raw whois data: ")
            print(w)
        if "dns-zt" in allowed:
            # DNS zone transfering test
            dns_helper = DNSHelper()
            dns_helper.scan(target)
        if "os-detect" in allowed:
            nmap_osmatch(target_ip, iface=config["iface"] if private else "")
        if "traceroute" in allowed:
            print(NOT_IMPLEMENTED + ": traceroute");
    else:
        print(f"[*] {target}({target_ip}) is private network.")
    print(f"[*] Finished basic scan for target {target}.")

def web_scan(config):
    subconf = config["web_scan"]
    allowed = subconf["subscans"]
    options = subconf["options"]
    target_ip = to_ip(config["target"])

    if "basic" in allowed:
        print(f"[*] Start base nmap scan for target {target_ip}...")
        try:
            args = f" -p{subconf['port']} -A "
            if "iface" in config: 
                args = args + "-e " + config["iface"]
            nmap = nmap3.NmapScanTechniques()
            ports = nmap.nmap_tcp_scan(target_ip, args = args)[str(target_ip)]
            ports = ports["ports"]
            if isinstance(ports, list):
                for p in ports:
                    # Processing 'scripts; if available
                    if "scripts" in p and isinstance(p["scripts"], list):
                        for s in p["scripts"]:
                             print(f"[*] -> {s['name']}: {s['raw']}")
        except Exception as ex:
            print("[!] Exception: {}".format(ex))
        print(f"[*] Finished nmap scan for target {target_ip}...")

    target = config["target"]
    if "http://" not in target:
        target = "http://" + target
    target = target + ":" + str(config["web_scan"]["port"])

    if "dirs" in allowed:
        print(f"[*] Start fuzzing target {target}...")
        try:
            dirs(target, options["dirs"])
        except Exception as ex:
            print(f"[!] Exception: {str(ex)}")
        print(f"[*] Dirscan finished for {target}")

    if "waf" in allowed:
        # wafw00f --format=json --output=- <target>
        ww = WafwoofCmdBuilder()
        parser = WafwoofResponseParser(
            ww
            .format()
            .output()
            .target(target)
            .run()
        )
        # [{'url': 'http://10.129.146.68:80', 'detected': False, 'firewall': 'None', 'manufacturer': 'None'}]
        result = parser.get()
        for r in result:
            if not r["detected"]:
                print(f"[*] No WAF detected for {r['url']}")
            else:
                print(f"[*] Detected WAF: {r['firewall']} from {r['manufacturer']}")

    if "subdomains" in allowed:
        print(NOT_IMPLEMENTED + ": subdomains");
        
    