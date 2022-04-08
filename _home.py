from flask import  Blueprint, render_template, session, redirect
from sqlalchemy import all_
home_bp = Blueprint('home_bp', __name__)

import _app

@home_bp.route('/home')
def home():
    if not session.get('logged_in'):
        print(session.get('logged_in'))
        return redirect('/logout')
    else:
        saldo = _app.Saldo.query.filter_by(id_conto = session.get('id_conto')).first()
        transazioni = _app.Transazione.query.filter_by(id_conto = session.get('id_conto')).all()    
    return render_template('home.html', session=session, transazioni = transazioni, saldo = saldo)
    
