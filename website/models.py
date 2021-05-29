from . import db
from flask_login import UserMixin #only use for login user
from sqlalchemy.sql import func

'''model to keep track of how many people have visited the site'''
class Visitor(db.Model):
    __tablename__ = "visitors"
    visitor_number = db.Column(db.Integer, primary_key=True, unique=True)
    date_visited = db.Column(db.DateTime, unique=True, default=func.now())

    def __repr__(self) -> str:
        return f"Visitor #{self.visitor_number} visited on {str(self.date_visited)}"

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # HAS to have info
    date_created = db.Column(db.String(10), nullable=False) # HAS to have info
    views = db.Column(db.Integer, nullable=False, default=0) 
    image_link = db.Column(db.String(150))
    video_link = db.Column(db.String(150), default="")
    project_link = db.Column(db.String(150), default="") # does this project have an external link?
    short_description = db.Column(db.String(100), nullable=False) # HAS to have info
    long_description = db.Column(db.String(3000), nullable=False) # HAS to have info
    importance_score = db.Column(db.Float, nullable=False, default=0.0) 

    def __init__(self, **kwargs) -> None:
        super(Project, self).__init__(**kwargs)

        # have to use this instead of using default because self.name needs to be defined first
        if 'image_link' not in kwargs:
            self.image_link = f"/static/images/projects/{self.name}.jpg" 

    def __repr__(self) -> str:
        return f"Project '{self.name}' created on {str(self.date_created)}: {self.short_description}"

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # HAS to have info
    number = db.Column(db.Integer, nullable=False, default=1)
    semester = db.Column(db.String(6), nullable=False, default="<2025") 
    prereqs = db.Column(db.String(100), nullable=False, default="None")
    description = db.Column(db.String(100), nullable=False, default="It's an MIT course")

    def __repr__(self) -> str:
        return f"Course '{self.number} {self.name}' taken in {self.semester}"
