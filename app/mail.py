
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)
import sendgrid 
from sendgrid.helpers.mail import *


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
           # send(email, subject, content)
            db, c = get_db()
            c.execute('INSERT INTO email (email, subject, content) VALUES(%s, %s, %s)', (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        else:
            for error in errors: 
                flash(errors)
    return render_template('mails/create.html')

def send(to, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    from_email = Email(current_app.config['FROM_EMAIL'])
    to_email = To(to)
    content = content('text/plain', content)
    mail = Mail(from_email, to_email, content)
    response =  sg.client.send.post(request_body=mail.get())
    print(response)