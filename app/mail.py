from flask import (
    Blueprint, render_template
)

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    db, c = get_db()

    c.execute('SELECT * FROM email')
    mails =c.fetchall()

    print(mails)
    return render_template('mails/index.html', mails=mails )