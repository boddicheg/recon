from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
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
