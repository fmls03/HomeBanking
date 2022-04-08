from flask import  Blueprint, render_template, session, redirect, request
from requests import request
from sqlalchemy import all_, desc
home_bp = Blueprint('home_bp', __name__)

import _app

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        print(session.get('logged_in'))
        return redirect('/logout')
    else:
        saldo = _app.Saldo.query.filter_by(id_conto = session.get('id_conto')).first()
        transazioni = _app.Transazione.query.filter_by(id_conto = session.get('id_conto')).order_by(desc(_app.Transazione.data)).all()  
        return render_template('home.html', session=session, transazioni = transazioni, saldo = saldo)
    
