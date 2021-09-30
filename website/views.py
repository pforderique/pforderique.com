from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Project, Visitor
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/', methods=["GET"]) # root page
def root():
    return redirect(url_for('views.home'))

@views.route('/home', methods=["GET"])
def home():
    '''UPDATE and return the # visitors the site has had'''
    rows = db.session.query(Visitor).count()
    print("ROWS:", rows)
    
    if rows == 0: 
        visitor_number = 1 
    else: 
        visitor_number = db.session.query(Visitor).order_by(Visitor.date_visited.desc()).first().visitor_number + 1

    #? delete past entries once database hits a threshold (memory management)
    if rows > 20: 
        db.session.query(Visitor).filter(Visitor.visitor_number < rows - 20).delete()

    #? add the visitor and commit em
    visitor = Visitor(visitor_number=visitor_number, date_visited=datetime.now())
    db.session.add(visitor)
    db.session.commit()
    print(visitor, "added!!!")

    # with open(r'website/static/docs/experience.json') as f:
    exp = [
        {
            "name":"Robotics Software Intern - NVIDIA",
            "logoPath":"/static/images/nvidia.png",
            "location":"Santa Clara, CA (Remote)",
            "duration":"Summer 2021",
            "description":"I had the opportunity to work with NVIDIA's Robotics Platform Team. The ROS Engineering Team strived to help bring NVIDIA's powerful hardware to the front lines with optimized algorithms to challenge their open-source, CPU versions of ROS2 packages. <br> <span style=\"font-weight: bold; color: black;\">See an article about the project </span><a href=\"https://developer.nvidia.com/blog/nvidia-ai-perception-coming-to-ros-developers/\" style=\"color: rgb(179, 122, 0);\">here</a> <span style=\"font-weight: bold; color: black;\"> and checkout the GitHub repo </span><a href=\"https://github.com/NVIDIA-AI-IOT/isaac_ros_apriltag\" style=\"color: rgb(179, 122, 0);\">here</a>",
            "bullets":[
                "Optimized standard ROS2 packages to run faster on NVIDIA hardware using internal APIs (C++)",
                "Reinforced project stability by writing multiple unit and integration tests (Python)",
                "Set software improvement goals based on performance benchmarking scripts (Python)",
                "Diagnosed and solved synchronization issues using time policy algorithms hidden in the implementation file (C++)",
                "Performed several code reviews (GitLab) and project document updates (Confluence)"
            ]        
        },
        {
            "name":"Software Engineer - MITOS",
            "logoPath":"/static/images/MIT_logo.png",
            "location":"Cambridge, MA (Remote)",
            "duration":"2020-2021",
            "description":"The MIT Office of Sustainability (MITOS) team focuses on preparing MIT for climate change. I worked with the Flood Risk Analysis team to see the impacts of future storm flooding on our campus.<br> <span style=\"font-weight: bold; color: black;\">See an article about my Fellow Story </span><a href=\"http://sustainability.mit.edu/article/student-fellow-stories-piero-orderique\" style=\"color: rgb(179, 122, 0);\">here</a>",
            "bullets":[
                "Cut down data processing time in half using SQL queries in ArcGIS Pro",
                "Created custom VBA functions for Excel to enhance project scalability and efficiency for future analysis",
                "Work helped identify a potential $600M+ worth of damage to university property from storm flooding simulation",
                "Design a Python package for reading and visualizing 300+ specialized data files from models using SciPy and matplotlib while practicing OOD",
                "Reduced space storage by 99.99% (from 1.1TB to < 1MB) by filtering large global datasets on a remote linux cluster",
                "Created data visualizations (matplotlib) for precipitation and temperature predictions in the Cambridge area"
            ]        
        },
        {
            "name":"Project Associate",
            "logoPath":"/static/images/borinquenfoods_logo.jpg",
            "location":"Columbus, GA",
            "duration":"2017-2020",
            "description":"Borinquen Foods is a family owned, Caribbean style restaurant/store that sells ethnic foods from Central and South America.        ",
            "bullets":[
                "Built and implemented an Arduino security system that sends messages to the owner when activated",
                "Updated security systems and feedback on a budget",
                "Quadrupled the restaurant's Google reviews and increased market reach by designing advertisements on Canva",
                "Digitized checking accounts using Excel"
            ]        
        },
        {
            "name":"Math Instructor",
            "logoPath":"/static/images/mathnasium_logo.jpg",
            "location":"Columbus, GA",
            "duration":"2020-2021",
            "description":"Mathnasium is a nationwide math tutoring business helping students and adults enjoy learning mathematics.",
            "bullets":[
                "Instructed adults for exams (GRE, ASVAB, etc.) and oversaw the instruction of 70+ K-12 students",
                "Received 100% positive evaluations and rescheduling rates",
                "Accommodated Spanish-speaking students and applied training to work with students with learning disabilities"
            ]
        }
    ]
    skillss = {
        "PROGRAMMING LANGUAGES":[
            "Python", "C++", "Java", "JavaScript", "SQL", "HTML/CSS", "LaTeX"
        ],
        "TECHNOLOGIES":[
            "Flask", "Socket IO","Excel", "Git", "ArcGIS", "ROS2", "Docker",
            "NumPy", "OpenCV", "Matplotlib", "Ubuntu Linux", "jQuery", "JIRA", 
            "Confluence", "GitHub/GitLab"  
        ],
        "CERTIFICATES":[
            "LinkedIn: PyTorch Essentials" , "OpenCV", "AI Foundations", 
            "Reccomendation Systems", "Learning Docker", "Advanced Python",
            "Esri: GIS Basics", "3D Visualization", "Querying Data", 
            "IBM: Machine Learning with Python", 
            "Microsoft: Introduction to C++", 
            "HarvardX: Data Science R Basics", 
            "UC San Diego: How Virtual Reality Works"
        ],
        "COURSES":[
            "MIT 14.01 Microeconomics",
            "MIT 18.01 Single Variable Calculus",
            "MIT 18.02 Multivariable Calculus",
            "MIT 24.05 Philosophy of Religion",
            "MIT 3.091 Solid State Chemistry",
            "MIT 6.0001 Introduction to Computer Science with Python",
            "MIT 6.006 Intro to Algorithms",
            "MIT 6.042 Mathematics for Computer Science (Discrete Mathematics)",
            "MIT 6.08 Intro to Embedded Systems",
            "MIT 6.901 Design Thinking and Innovation",
            "MIT 6.UAT Oral Communication",
            "MIT 7.012 Introductory Biology",
            "MIT 8.01 Classical Mechanics",
            "MIT 8.02 Electricity and Magnetism"
        ]
    }
    #   experience_data = json.load(f)
    experience_data = exp #json.load(exp)

    # with open(r'website/static/docs/skills.json') as f:
    skills =  skillss#json.load(skillss)

    return render_template("home.html", 
        user=current_user, 
        visitor_number=visitor_number, 
        experience_data=experience_data,
        skills=skills)

@views.route('/projects', methods=["GET"])
def projects():
    '''RETURN projects based on search OR GET most popular ~10 projects to display side by side'''
    name = request.args.get('name')
    
    if name:
        queryname = f"%{name}%"
        featured_projects = db.session.query(Project).filter(Project.name.like(queryname)
        ).order_by(Project.importance_score.desc()).limit(10).all()
    else:
        featured_projects = db.session.query(Project).order_by(Project.importance_score.desc()).limit(10).all()

    #* have to convert featured_projects into tuple list for jijna rendering (p1,p2), (p3,p4), ...
    size = len(featured_projects)
    tupled_projects = []

    for idx in range(0, size, 2):
        p1 = featured_projects[idx]

        if idx + 1 < size: 
            p2 = featured_projects[idx+1]
        else: 
            p2 = ""

        tupled_projects.append((p1,p2))

    return render_template("projects.html", projects=tupled_projects)

@views.route('/project/<name>', methods=["GET"])
def project(name):
    '''ADD 0.1 to project's popularity score'''
    project = db.session.query(Project).filter(Project.name==name).first()

    if project is not None:
        project.importance_score += 0.0625
        project.views += 1
        db.session.commit()

    return render_template("single_project.html", project=project)

@views.route("/resume", methods=["GET"])
def resume():
    '''GET all courses and display them under the resume'''
    courses = []
    return render_template("resume.html", courses=courses)