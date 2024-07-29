from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import atexit
import uuid
import datetime

# Create a base class for declarative class definitions
Base = declarative_base()

# -----------------------------------------------------------------------------
# Tables
class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uuid = Column(String, nullable=False)
    target = Column(String, nullable=False)
    description = Column(String)
    resources = Column(Integer, nullable=False)
    date_updated = Column(String, nullable=False)

class Commands(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    project_uuid = Column(String, nullable=False)
    command = Column(String, nullable=False)
    output = Column(String, nullable=False)
# -----------------------------------------------------------------------------
    
class DBSession:
    def __init__(self, db_path) -> None:
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        atexit.register(self.destuctor)
        
    def destuctor(self):
        self.session.close()
        
# -----------------------------------------------------------------------------
# Projects methods
    def add_project(self, data):
        keys = ["name", "description"]
        for k in keys:
            if k not in data.keys():
                print(f"-> Can't find key {k} in params")
                return

        self.session.add(Projects(
            uuid=str(uuid.uuid4()),  
            name=data["name"],
            target=data["target"],
            description=data["description"],
            resources=0,
            date_updated=datetime.datetime.now()
        ))
        
        self.session.commit()
        
    def get_project_data(self, uuid):
        data = self.session.query(Projects).filter_by(uuid=uuid).first()
        
        result = {
            "name": data.name,
            "uuid": data.uuid,
            "target": data.target
        }
    
        return result
        
    def get_projects(self):
        projects = self.session.query(Projects).all()
        result = []
        for project in projects:
            result.append({
                "uuid": project.uuid,
                "name": project.name,
                "target": project.target,
                "description": project.description,
                "resources": project.resources,
                "date_updated": project.date_updated
            })
        return result
# -----------------------------------------------------------------------------
    def add_project_cmd(self, data):
        keys = ["command", "project_uuid"]
        for k in keys:
            if k not in data.keys():
                print(f"-> Can't find key {k} in params")
                return

        self.session.add(Commands(
            uuid=str(uuid.uuid4()),  
            project_uuid=data["project_uuid"],
            command=data["command"],
            output="Test Output"
        ))
        
        self.session.commit()

    def get_command_data(self, uuid):
        cmd = self.session.query(Commands).filter_by(uuid=uuid).first()
        
        result = {
            "uuid": cmd.uuid,
            "command": cmd.command,
            "output": cmd.output,
            "project_uuid": cmd.project_uuid
        }
    
        return result
        
    def get_project_cmds(self, project_uuid):
        cmds = self.session.query(Commands).filter_by(project_uuid=project_uuid).all()
        result = []
        for cmd in cmds:
            result.append({
                "uuid": cmd.uuid,
                "command": cmd.command,
                "output": cmd.output,
            })
        return result