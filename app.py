from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    list = db.Column(db.Text, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Event %r>' % self.name


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.name

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)
    # return render_template('index.html')

@app.route('/addEvent/', methods=['POST', 'GET'])
def addEvent():
    if request.method == 'POST':
        name = request.form['eventName']
        details = request.form['eventDetails']
        print(name)
        print(details)
        newEvent = Event(name=name, details=details)
        try:
            db.session.add(newEvent)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your event."
    else:
        return render_template('addEvent.html')

@app.route('/eventDetails/<int:id>')
def eventDetails(id):
    event = Event.query.get_or_404(id)
    return render_template('eventDetails.html', name=event.name, details=event.details)

@app.route('/delete/<int:id>')
def deleteEvent(id):
    event = Event.query.get_or_404(id)
    try:
        db.session.delete(event)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting your event"


if __name__ == '__main__':
    app.run(debug=True)
