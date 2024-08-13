import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
TMP = ROOT / "tmp"

VHOST_WL = str(TMP / "SecLists/Discovery/Web-Content/common.txt")
PARAMS_WL = str(TMP / "SecLists/Discovery/Web-Content/common.txt")
DIRS_WL = str(TMP / "SecLists/Discovery/Web-Content/common.txt")

print(VHOST_WL)
UA = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
XFF = "X-Forwarded-For: 127.0.0.1"
TARGET_TEMPL = "{target}"

def _traceroute(target):
    return "_traceroute"

def _geolocation(target):
    return "_geolocation"

def _dummy(target):
    return "_dummy"

non_shell_commands = {
    "_troute": _traceroute,
    "_geoloc": _geolocation,
    "_whois": _dummy,
    "_dns": _dummy,
    "_headers": _dummy,
    "_firewall": _dummy,
    "_ssl": _dummy,
    "_blocklist": _dummy,
}

def is_non_shell_command(cmd):
    if not isinstance(cmd, list):
        print("Pass cmd as list")
        return False

    return cmd[0] in non_shell_commands.keys()

def process_non_shell(cmd):
    if cmd[0] in non_shell_commands.keys():
        return non_shell_commands[cmd[0]](cmd)
    
    return ""

command_aliases = {
    "_vhosts": [
        "ffuf", "-ac", "-mc", "all", "-c", "-u", f"https://{TARGET_TEMPL}", "-w", f"{VHOST_WL}", "-H", f"'Host: FUZZ.{TARGET_TEMPL}'", "-H", f"'{UA}'", "-s", "-json"
    ],
    "_params": [
        "ffuf", "-mc", "all", "-c", "-H", f"'{UA}'", "-H", f"'{XFF}'", "-u", f"\"https://{TARGET_TEMPL}?FUZZ=abcd\"", "-w", f"{PARAMS_WL}", "-ac", "-s", "-json"
    ],
    "_pscan": [
        "nmap", "-sS", "-T4", "-A", "-p-", f"{TARGET_TEMPL}", "--min-rate", "1000", "--max-retries", "3"
    ],
    "_dscan": [
        "ffuf", "-u", f"https://{TARGET_TEMPL}/FUZZ", "-w", f"{DIRS_WL}", "-H", f"'{UA}'", "-H", f"'{XFF}'", "-D", "-e", "js,php,bak,txt,asp,aspx,jsp,html,zip,jar,sql,json,old,gz,shtml,log,swp,yaml,yml,config,save,rsa,ppk", "-ac", "-c", "-mc", "all", "-s", "-json"
    ]
}

def _ffuf_json_processor(response_line):
    response_line = response_line.strip()
    if response_line:
        try:
            result = json.loads(response_line)
            response_line = f"[{result["status"]}, {result["length"]}b] [{result["url"]}]({result["url"]})"
            if result["redirectlocation"]:
                response_line += f", redirect to [{result["redirectlocation"]}]({result["redirectlocation"]})"
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        return ""

    return response_line
            
response_processors = {
    "ffuf": _ffuf_json_processor,
}

def process_command(cmd):
    print(cmd)
    # cmd format:
    # ["_vhosts", "google.com"]
    if not isinstance(cmd, list):
        print("Pass cmd as list")
        return cmd

    if len(cmd) == 2:
        alias = cmd[0]
        target = cmd[1]
        
        full_command = []
        for chunk in command_aliases[alias]:
            full_command.append(chunk.replace(TARGET_TEMPL, target))
        return full_command
    else:
        return cmd
    
def process_command_response(cmd, line):
    if line:
        try:
            if len(cmd) > 0:
                return response_processors[cmd[0]](line)
        except Exception as e:
            print(f"An error occurred: {e}")

    return line