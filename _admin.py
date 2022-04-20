from flask import Flask, Blueprint, redirect, render_template, request, session
from sqlalchemy import *
import datetime


admin_bp = Blueprint('admin_bp', __name__)

import _app

@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect('/logout')
    else:
        users = _app.User.query.all()
        users.pop(2)
    return render_template('admin.html', users = users)


@admin_bp.route('/<int:idx>/invia_denaro', methods=['POST', ])
def invia_denaro(idx):
    if session.get('logged_in') == True:
        user = _app.User.query.filter_by(id_user = idx).first()

        bonifico = _app.Transazione(session.get('username'), user.conto.iban, 1000, datetime.datetime.now(), "Denaro inviato dall'admin", user.conto.id_conto)

        _app.db.session.add(bonifico)
        _app.db.session.commit()        
        _app.db.session.refresh(bonifico)

        user.conto.saldo.saldo_disponibile += 1000
        user.conto.saldo.saldo_contabile += 1000

        _app.db.session.merge(user)
        _app.db.session.commit()
        _app.db.session.refresh(user)
    
    else:
        return redirect('/redirecting')

    return redirect('/admin')


@admin_bp.route('/<int:idx>/svuota_saldo', methods=['POST', ])
def svuota_saldo(idx):
        if session.get('logged_in') == True:
            user = _app.User.query.filter_by(id_user = idx).first()
            
            bonifico = _app.Transazione(session.get('username'), user.conto.iban, -user.conto.saldo.saldo_disponibile, datetime.datetime.now(), "Saldo svuotato dall'admin", user.conto.id_conto)

            _app.db.session.add(bonifico)
            _app.db.session.commit()        
            _app.db.session.refresh(bonifico)

            saldo = _app.Saldo.query.filter_by(id_conto=user.conto.id_conto).first()
            saldo.saldo_disponibile -= saldo.saldo_disponibile
            saldo.saldo_contabile -= saldo.saldo_contabile

            _app.db.session.merge(saldo)
            _app.db.session.commit()
            _app.db.session.refresh(saldo)
        else:
            return redirect('/redirecting')
        return redirect('/admin')

