import threading
import datetime
import atexit
import subprocess
import signal
import os
import time

from database.models import *
from modules.commands import *

DB_PATH = "db.sqlite"
TEMPLATE_TARGET = "{target}"
MARKDOWN_NEWLINE = "\n"
CACHE_FOLDER = "tmp"

def current_ts():
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return f"[{formatted_now}]"

class ShellManager():
    def __init__(self, root, uuid, cmd) -> None:
        self.lock = threading.Lock()
        self.cmd = cmd
        self.root = root
        self.uuid = uuid
        self.output = ""
        self.running = False
        self.process = None
        self.thread = threading.Thread(target=self.run_in_thread)

        atexit.register(self.stop)

    def get_output(self):
        with self.lock:
            return self.output
    
    def get_status(self):
        with self.lock:
            return self.running

    def run_in_thread(self):
        cmd = ""
        with self.lock:
            self.output += f"{current_ts()} UUID: {self.uuid}{MARKDOWN_NEWLINE}"
            cmd = self.cmd

        if cmd == "":
            with self.lock:
                self.output += f"{current_ts()} Empty input command!{MARKDOWN_NEWLINE}"
                self.running = False
            return
        
        try:
            # Change directory to CACHE_FOLDER in case some install commands
            cache = self.root + "/../" + CACHE_FOLDER
            print(cache, self.root)
            if not os.path.exists(cache):
                os.mkdir(cache)
            os.chdir(cache)

            # Start subprocess
            cmds = []
            if "\n" in cmd:
                cmds = cmd.split("\n")
            else:
                cmds = [cmd]

            for c in cmds:
                start = time.time_ns() // 1_000_000
                cmd_tokens = c.split(" ")
                
                if is_non_shell_command(cmd_tokens):
                    print("is_non_shell_command + ")
                    result = process_non_shell(cmd_tokens)
                    with self.lock:
                        self.output += f"\n {current_ts()} ---> {" ".join(cmd_tokens)} <----{MARKDOWN_NEWLINE}\n"
                        self.output += f"{current_ts()} {result.strip()}{MARKDOWN_NEWLINE}"
                else:
                    cmd_tokens = process_command(cmd_tokens)
                    self.output += f"\n {current_ts()} ---> {" ".join(cmd_tokens)} <----{MARKDOWN_NEWLINE}\n"

                    self.process = subprocess.Popen(
                        cmd_tokens, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        text=True, 
                        start_new_session=True, 
                        encoding='utf-8', 
                    )

                    if not self.process:
                        with self.lock:
                            self.output += f"{current_ts()} Unable to create subpocess!{MARKDOWN_NEWLINE}"
                            self.running = False
                        return
                    
                    self.process.stdin.flush()
                    
                    # Read and print the output in real-time
                    while True:
                        with self.lock:
                            if not self.running:
                                break
                        
                        output = self.process.stdout.readline()
                        if output == '' and self.process.poll() is not None:
                            break
                        if output:
                            with self.lock:
                                output = process_command_response(cmd_tokens, output)
                                if output:
                                    self.output += f"{current_ts()} {output.strip()}{MARKDOWN_NEWLINE}"
                
                elapsed = time.time_ns() // 1_000_000 - start
                with self.lock:
                    self.output += f"{current_ts()} Finished processing in {elapsed:.2f}ms!{MARKDOWN_NEWLINE}"
                
                if self.process:  
                    self.process.kill()
                    self.process = None
                
            self.running = False

        except Exception as e:
            print(f"An error occurred: {e}")
            with self.lock:
                self.output += f"{current_ts()} An error occurred: {e}! {MARKDOWN_NEWLINE}"
                self.running = False
    
    def run(self):
        with self.lock:
            self.running = True

        self.thread.start()

    def stop(self):
        with self.lock:
            self.running = False
            if self.process:
                self.process.send_signal(signal.SIGTERM)
        if self.thread.is_alive():
            self.thread.join()

class ProjectsController():
    def __init__(self, root) -> None:
        self.database = DBSession(DB_PATH)
        self.root = root
        self.lock = threading.Lock()
        self.processing_cmds = {}
        
    def get_projects(self):
        return self.database.get_projects()
    
    def add_project(self, data):
        return self.database.add_project(data)
    
    def get_project(self, uuid):
        return self.database.get_project_data(uuid)
    
    def get_project_cmds(self, uuid):
        commands = self.database.get_project_cmds(uuid)
        for cmd in commands:
            cmd["output"] = self.get_output(uuid)
        return commands
    
    def add_command(self, uuid, command, title, is_global):
        return self.database.add_project_cmd({
            "command": command,
            "project_uuid": uuid,
            "title": title,
            "is_global": is_global
        })

    def start_execution(self, uuid):
        with self.lock:
            if uuid in self.processing_cmds.keys() and \
                self.processing_cmds[uuid].get_status() :
                print("Command already processing")
                return

        # Get command by uuid
        command_data = self.database.get_command_data(uuid)
        # Get project by parent uuid from command
        parent_project = self.database.get_project_data(command_data["project_uuid"])
        # Replace target from project in command string
        cmd = str(command_data["command"]).replace(TEMPLATE_TARGET, parent_project["target"])
        # Run command
        with self.lock:
            self.processing_cmds[uuid] = ShellManager(self.root, uuid, cmd)
            self.processing_cmds[uuid].run()

    def stop_execution(self, uuid):
        print("stop_execution +")
        if uuid in self.processing_cmds:
            self.processing_cmds[uuid].stop()
        # TODO: decide if we should delete command after stop
        # del self.processing_cmds[uuid]
        print("stop_execution -")
    
    def get_output(self, uuid):
        with self.lock:
            if uuid in self.processing_cmds:
                return self.processing_cmds[uuid].get_output()
            else:
                return ""

    def get_status(self, uuid):
        with self.lock:
            if uuid in self.processing_cmds:
                return self.processing_cmds[uuid].get_status()
            return False
        
    def detete_command(self, uuid):
        self.stop_execution(uuid)
        self.database.delete_project_cmd(uuid)
        
    def get_global_cmds(self):
        result = []
        commands = self.database.get_global_cmds()
        for cmd in commands:
            result.append({
                "label": cmd["command"],
                "value": cmd["command"],
            })
        return result
