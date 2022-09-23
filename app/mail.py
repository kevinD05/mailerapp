from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    db, c = get_db()

    c.execute('SELECT * FROM email')
    mails =c.fetchall()

    
    return render_template('mails/index.html', mails=mails )

@bp.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Email es obligatorio') 
        if not subject:
            errors.append('asunto es obligatorio') 
        if not content:
            errors.append('contenido es obligatorio') 

        if len(errors) == 0:
            db, c = get_db()
            c.execute('INSERT INTO email (email, subject, content) VALUES(%s, %s, %s)', (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        else:
            for error in errors: 
                flash(errors)
    return render_template('mails/create.html')

def send(to, subject, content):
    sg = sendgrid.sendGriAPIclient(api_key=current_app.config['SENDGRID_KEY'])