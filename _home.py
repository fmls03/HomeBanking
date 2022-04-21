from flask import Flask,  Blueprint, render_template, session, redirect, request
from sqlalchemy import all_, desc
home_bp = Blueprint('home_bp', __name__)

import _app

@home_bp.route('/home', methods=['GET', 'POST'])
async def home():
    if not session.get('logged_in'):
        return redirect('/logout')
    else:

        username = session.get('username')

        saldo = _app.Saldo.query.filter_by(id_conto = session.get('id_conto')).first()

        transazioni = await get_data()

        return render_template('home.html', session=session, transazioni = transazioni, saldo = saldo, username = username)
    



async def get_data():

    transazioni_ricevute = _app.Transazione.query.filter_by(id_conto = session.get('id_conto')).order_by(desc(_app.Transazione.data)).all()
    transazioni_effettuate = _app.Transazione.query.filter_by(user_mittente = session.get('username')).order_by(desc(_app.Transazione.data)).all()
        
    for t in transazioni_effettuate:
        t.importo = -t.importo
            
    transazioni = [*transazioni_effettuate, *transazioni_ricevute]
    transazioni.sort(key=lambda x: x.data, reverse=True)
    
    return transazioni