from database.models import *

DB_PATH = "db.sqlite"

class ProjectsController():
    def __init__(self, root) -> None:
        self.database = DBSession(DB_PATH)
        
    def get_projects(self):
        return self.database.get_projects()
    
    def add_project(self, data):
        return self.database.add_project(data)