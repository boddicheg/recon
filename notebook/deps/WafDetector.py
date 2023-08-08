import subprocess
import json

class WafwoofCmdBuilder():
    def __init__(self):
        super().__init__()
        self.cmd = "wafw00f "

    def format(self, f = "json"):
        self.cmd += " --format=" + f
        return self
    
    def output(self):
        self.cmd += " --output=-"
        return self

    def target(self, target):
        self.cmd += " " + target
        return self

    def get(self):
        return self.cmd

    def run(self):
        sub_proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True)

        try:
            out, _ = sub_proc.communicate()
            return out

        except Exception as e:
            sub_proc.kill()
            print("[WafWoof] Running failed with error: {0}".format(e))
            return None
        
class WafwoofResponseParser():
    def __init__(self, response):
        try:
            self.json = json.loads(response)
        except Exception as e:
            print("[Wafwoof] Parsing failed with error: {0}".format(e))
            self.json = None

    def get(self):
        return self.json