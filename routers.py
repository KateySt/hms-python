from flask import Blueprint, render_template, redirect, url_for, flash

from db import db
from forms import EventForm
from models import Event

app = Blueprint('app', __name__)


@app.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        flash('Event added.', 'success')
        return redirect(url_for('app.index'))
    else:
        flash('Error.', 'warning')
    return render_template('add_event.html', form=form)


@app.route('/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('app.index'))
