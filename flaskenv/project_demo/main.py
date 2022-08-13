import py_compile
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body
        
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/notes/create", methods=["GET", "POST"])
def create_note():
    if request.method == "GET": 
        return render_template("create_note.html") 
    else: title = request.form["title"] 
    body = request.form["body"]
    
    note = Note(title=title, body=body)
    db.session.add(note) 
    db.session.commit()
    return redirect("/")

@app.route('/notes')
def RetrieveDataList():
    notes = Note.query.all()
    return render_template('notes.html',notes = notes)


@app.route('/notes/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    note = Note.query.filter_by(id=id).first()
    if request.method == 'POST':
        if note:
            db.session.delete(note)
            db.session.commit()
            return redirect('/notes')
        
    return render_template('delete.html')


@app.route('/notes/update/<int:id>',methods = ['GET','POST'])
def update(id):
    note = Note.query.filter_by(id=id).first()
    if request.method == 'POST':
        if note:
            db.session.delete(note)
            db.session.commit()

            title = request.form['title']
            body = request.form['body']
            note = Note(title=title, body=body)
 
            db.session.add(note)
            db.session.commit()
            return redirect('/notes')
         
        return f"Note with id = {id} Does not exist"
 
    return render_template('update.html', note = note)









if __name__ == "__main__":
    app.run(debug=True)
    