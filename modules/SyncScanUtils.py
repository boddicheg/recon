import socket
import nmap3
import wfuzz
import whois
from modules.WafDetector import *
from modules.GeoLocation import *

def not_impl(target):
    return {
        "not_impl": None
    }

def host_to_ip(target):
    if "http" in target:
        target = target.split("://")[1]
    return { 
        "ip": socket.gethostbyname(target) 
    }
    
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

def osmatch(target):
    nmap = nmap3.Nmap()
    os_results = nmap.nmap_os_detection(target)[target]["osmatch"]
    return os_results
    
def ports(target, top = 100):
    import nmap3
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(target, top)[target]["ports"]
    return results

def geo(target):
    g = GeoLocation("")
    return g.get(target)

def who(target):
    return whois.whois(target)

def dirs(target, config):
    results = []
    path = "assets/SecLists/"
    wls = config["wordlists"]
    
    session = wfuzz.FuzzSession(url=target + "/FUZZ")
    
    for wl in wls:
        file = path + wl
        for r in session.fuzz(hc=config["skip_codes"], payloads=[("file", dict(fn = file))]):
            template = {
                "code": r.code,
                "uri": r.description,
                "request": r.history
            }
            results.append(template)

    return results
        