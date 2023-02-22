import socket
from modules.WafDetector import *

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