from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Project, Visitor
from . import db
import json
from datetime import datetime

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

    return render_template("home.html", user=current_user, visitor_number=visitor_number)

@views.route('/projects', methods=["GET"])
def projects():
    '''RETURN projects based on search OR GET most popular ~10 projects to display side by side'''
    name = request.args.get('name')
    
    if name:
        queryname = f"%{name}%"
        featured_projects = db.session.query(Project).filter(Project.name.like(queryname)).limit(10)
    else:
        featured_projects = db.session.query(Project).order_by(Project.importance_score.desc()).limit(10)

    return render_template("projects.html", projects=featured_projects)

@views.route('/project/<name>', methods=["GET"])
def project(name):
    '''ADD 0.1 to project's popularity score'''
    project = db.session.query(Project).filter(Project.name==name).first()

    if project is not None:
        project.importance_score += 0.0625
        db.session.commit()

    return render_template("single_project.html", project=project)

@views.route("/resume", methods=["GET"])
def resume():
    '''GET all courses and display them under the resume'''
    courses = []
    return render_template("resume.html", courses=courses)