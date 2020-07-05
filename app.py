from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open("config.json", "r") as fp:
    params = json.load(fp)["params"]



app = Flask(__name__)

if params["run"] == "dev":
  app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

db = SQLAlchemy(app)

class Links(db.Model):
    '''
    Links Table for FileO
    '''
    sr_no = db.Column(db.Integer, nullable=False)
    originalLink = db.Column(db.String(11180), nullable=False)
    FLink = db.Column(db.String(1880), primary_key=True, nullable=False)


class Config(db.Model):
    '''
    To get configurations from database!
    '''
    sr_no = db.Column(db.Integer,primary_key=True, nullable=False)
    key = db.Column(db.String(1102), nullable=False)
    value = db.Column(db.String(1120), nullable=False)





@app.route('/')
@app.route("/l")
@app.route('/index')
def index():
    data = Config.query.filter_by(key="creatorLink").first()
    link = data.value
    return redirect(link, code=302)


@app.route('/l/<string:link>' , methods=['GET'])
def getLink(link):
    customLink = Links.query.filter_by(FLink=link).first()
    if customLink:
        originalLink = customLink.originalLink
        return redirect(originalLink, code=302)
    else:
        data = Config.query.filter_by(key="creatorLink").first()
        link = data.value
        return render_template("ShortLink.html",link=link)
   

@app.errorhandler(404)
def pageNotFound(error):
    data = Config.query.filter_by(key="creatorLink").first()
    link = data.value
    return render_template("404.html", link=link)

if params["run"] == "dev":
    app.run(debug=True, port=5500)
else:
    app.run(debug=False)
