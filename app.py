from flask import  Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)




class Note(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(100))
    complete =db.Column(db.Boolean())
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    finito = db.Column(db.String(100))

    



@app.route('/')
def home():

    incomplete =Note.query.filter_by(complete=False).order_by(desc(Note.date)).all()
    complete = Note.query.filter_by(complete=True).order_by(desc(Note.date)).all()

    return render_template('home.html', incomplete=incomplete, complete=complete, delete=delete)


@app.route('/add', methods=['POST'])
def add():
    note = Note(text=request.form['todoitem'], complete=False, finito=request.form['DateBut'])
    db.session.add(note)
    db.session.commit()
    return redirect (url_for('home'))


@app.route('/complete/<id>')
def complete(id):
    note = Note.query.filter_by(id=int(id)).first()
    note.complete = True
    note.finito = "0000-00-00"
    db.session.commit()

    return redirect (url_for('home'))
    
@app.route('/incomplete/<id>', methods=['POST'])
def incomplete(id):
    note = Note.query.filter_by(id=int(id)).first()
    note.complete = False
    note.finito = request.form['RecoDateBut']
    db.session.commit()

    return redirect (url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    note = Note.query.filter_by(id=int(id)).first()
    db.session.delete(note)
    db.session.commit()

    return redirect (url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
