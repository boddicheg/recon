import socket
import nmap3

def to_ip(target):
    if "http" in target:
        target = target.split("://")[1]
    return socket.gethostbyname(target)

def wafwoof(target):
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
    
def nmap_ports(target, top = 100, iface = ""):
    nmap = nmap3.Nmap()
    args = ""
    if iface:
        args = "-e " + iface
    try:
        ports = nmap.scan_top_ports(target, top, args = args)
        print(ports)
    except Exception as ex:
        print("[!] Exception: {}".format(ex))

def geo(target):
    g = GeoLocation("")
    return { "geo": g.get(target) }

def whois(target):
    return { "whois": whois.whois(target) }