from flask import Flask, Blueprint, redirect, render_template, request, session
from sqlalchemy import *
import datetime
import operator
import time


admin_bp = Blueprint('admin_bp', __name__)

import _app

@admin_bp.route('/admin', methods = ['GET', 'POST'])
async def admin():
    if not session.get('logged_in'):
        return redirect('/logout')
    else:
        users = get_data()
    return render_template('admin.html', users = users)

def get_data():
    us = 'admin'
    users = _app.User.query.all()
    for user in users:
        if user.username == us:
            users.remove(user)
    return users


@admin_bp.route('/admin/invia_denaro/<int:idx>', methods=['POST', ])
def invia_denaro(idx):
    if session.get('logged_in') == True:
        user = _app.User.query.filter_by(id_user = idx).first()

        transazione = _app.Transazione(session.get('username'), user.conto.iban, 1000, datetime.datetime.now(), "Denaro inviato dall'admin", user.conto.id_conto)

        _app.db.session.add(transazione)
        _app.db.session.commit()

        user.conto.saldo.saldo_disponibile += 1000
        user.conto.saldo.saldo_contabile += 1000

        _app.db.session.merge(user)
        _app.db.session.commit()

        _app.db.session.remove()

        
    else:
        return redirect('/redirecting')

    return redirect('/admin')


@admin_bp.route('/admin/svuota_saldo/<int:idx>', methods=['POST', ])
def svuota_saldo(idx):
        if session.get('logged_in') == True:
            user = _app.User.query.filter_by(id_user = idx).first()
            
            saldo = _app.Saldo.query.filter_by(id_conto=user.conto.id_conto).first()
            saldo.saldo_disponibile -= saldo.saldo_disponibile
            saldo.saldo_contabile -= saldo.saldo_contabile

            _app.db.session.merge(saldo)
            _app.db.session.commit()

            _app.db.session.remove()
            
        else:
            return redirect('/redirecting')
        return redirect('/admin')

