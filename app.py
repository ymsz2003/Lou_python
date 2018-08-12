from datetime import datetime
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy

import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'

db = SQLAlchemy(app)
class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)
    def __init__(self,title,category,content,created_time = None):
        self.title = title
        if created_time == None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category
        self.content = content

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    files = db.relationship('File')
    def __init__(self,name):
        self.name = name



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
@app.route('/')
def index():
    return render_template('index.html', text=File.query.all())
@app.route('/files/<filename>')
def file_index(filename):
    try:
        file_item = File.query.get(filename)
    except:
        abort(404)
    return render_template('file.html', file_item = file_item)


