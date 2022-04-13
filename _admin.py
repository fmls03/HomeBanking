from flask import Flask, Blueprint, redirect, render_template, request
from sqlalchemy import *

admin_bp = Blueprint('admin_bp', __name__)

import _app

@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin():
    users = _app.User.query.all()
    if request.method == 'POST':
        if request.form['svuota-saldo']:
            saldo = _app.Saldo.query.filter_by(id_conto=request.form['svuota-saldo']).first()
            saldo.saldo_disponibile = 0
            saldo.saldo_contabile = 0

            _app.db.session.merge(saldo)
            _app.db.session.commit()
            _app.db.session.refresh(saldo)

            print(saldo.saldo_disponibile)
    # Rimuovo dalla lista l'utente admin
    users.pop(2)
    return render_template('admin.html', users = users)