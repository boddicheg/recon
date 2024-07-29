from database.models import *
import threading
import time
import atexit

DB_PATH = "db.sqlite"
TEMPLATE_TARGET = "{target}"
MARKDOWN_NEWLINE = "\n"

class ShellManager():
    def __init__(self, uuid, cmd) -> None:
        self.lock = threading.Lock()
        self.cmd = cmd
        self.uuid = uuid
        self.output = ""
        self.running = False
        self.thread = threading.Thread(target=self.run_in_thread)

        atexit.register(self.stop)

    def get_output(self):
        with self.lock:
            return self.output
    
    def get_status(self):
        with self.lock:
            return self.running

    def run_in_thread(self):
        with self.lock:
            self.output += f"UUID: {self.uuid}{MARKDOWN_NEWLINE}"

        count = 100
        while True:
            with self.lock:
                if not self.running:
                    break
            if count <= 0:
                break

            time.sleep(1)
            with self.lock:
                self.output += f"Output: {count}{MARKDOWN_NEWLINE}"
            count -= 1

        with self.lock:
            self.output += f"Finished processing!{MARKDOWN_NEWLINE}"
            self.running = False
    
    def run(self):
        with self.lock:
            self.running = True

        self.thread.start()

    def stop(self):
        print("stop +")
        with self.lock:
            self.running = False
        if self.thread.is_alive():
            self.thread.join()
        print("stop -")

class ProjectsController():
    def __init__(self, root) -> None:
        self.database = DBSession(DB_PATH)
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
    
    def add_command(self, uuid, command):
        return self.database.add_project_cmd({
            "command": command,
            "project_uuid": uuid
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
            self.processing_cmds[uuid] = ShellManager(uuid, cmd)
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

