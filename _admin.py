from flask import Flask, Blueprint, redirect, render_template, request, session
from sqlalchemy import *

admin_bp = Blueprint('admin_bp', __name__)

import _app

@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect('/logout')
    else:
        users = _app.User.query.all()
        if request.method == 'POST':
            if request.form['svuota-saldo'] != None:
                print(request.form['svuota-saldo'])
                user = _app.User.query.filter_by(id_user = request.form['svuota-saldo']).first()
                saldo = _app.Saldo.query.filter_by(id_conto=user.conto.id_conto).first()
                saldo.saldo_disponibile = 0
                saldo.saldo_contabile = 0

                _app.db.session.merge(saldo)
                _app.db.session.commit()
                _app.db.session.refresh(saldo)

            if request.form['elimina-utente'] != None:
                print(request.form['elimina-utente'])
                user = _app.User.query.filter_by(id_user = request.form['elimina-utente']).first() 
                conto = _app.Conto.query.filter_by(id_user = user.id_user).first()
                saldo = _app.Saldo.query.filter_by(id_conto =user.conto.id_conto).first()

                _app.db.session.delete(user)
                _app.db.session.delete(conto)
                _app.db.session.delete(saldo)
                _app.db.session.commit()    

        # Rimuovo dalla lista l'utente admin

        users.pop(2)
    return render_template('admin.html', users = users)