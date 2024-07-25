from database.models import *

DB_PATH = "db.sqlite"

class ProjectsController():
    def __init__(self, root) -> None:
        self.database = DBSession(DB_PATH)
        
    def get_projects(self):
        return self.database.get_projects()
    
    def add_project(self, data):
        return self.database.add_project(data)
    
    def get_project(self, uuid):
        return self.database.get_project_data(uuid)
    
    def get_project_cmds(self, uuid):
        return self.database.get_project_cmds(uuid)
    
    def add_command(self, uuid, command):
        return self.database.add_project_cmd({
            "command": command,
            "project_uuid": uuid
        })