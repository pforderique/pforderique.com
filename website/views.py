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

    with open('website\static\docs\experience.json') as f:
      experience_data = json.load(f)

    with open('website\static\docs\skills.json') as f:
      skills = json.load(f)
      print(skills)

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