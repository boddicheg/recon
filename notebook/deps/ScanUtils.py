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
# Waf detection
from deps.WafDetector import *

FTP_PORT = 21
TELNET_PORT = 23
SMB_PORT = 445

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

def test_ports(target, port_nums=[]):
    # FTP
    if FTP_PORT in port_nums:
        ftp_cmds = [
            'LIST',
            'PWD'
        ]
        test_ftp(target, cmds=ftp_cmds);
    # Telnet
    if TELNET_PORT in port_nums:
        telnet_cmds = [
            'ls',
        ]
        test_telnet(target, cmds=telnet_cmds);
    # SMB
    if SMB_PORT in port_nums:
        test_smb(target)
            
def test_waf(target):
    # wafw00f --format=json --output=- <target>
    ww = WafwoofCmdBuilder()
    parser = WafwoofResponseParser(
        ww
        .format()
        .output()
        .target(target)
        .run()
    )
    return {"waf" : parser.get()}

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
        ports = nmap.scan_top_ports(target, top, args = args)[target]["ports"]
        if isinstance(ports, list):
            print(f"[*] Found {len(ports)} port(s):")
            for p in ports:
                keys = ["name", "product", "version"]
                data = {}
                for k in keys:
                    data[k] = "N/A" if k not in p['service'].keys() else p['service'][k]
                print(f"[*] {p['portid']}/{p['protocol']} {p['state']}, service {data['name']}({data['product']}/{data['version']})")
                ports_ids.append(int(p['portid']))
    except Exception as ex:
        print("[!] Exception: {}".format(ex))

    return ports_ids

def geo(target):
    g = GeoLocation("")
    return { "geo": g.get(target) }

def whois(target):
    return { "whois": whois.whois(target) }