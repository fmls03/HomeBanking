from flask import Flask, Blueprint, render_template, request, session
from datetime import date
from sqlalchemy import *

bonifico_bp = Blueprint('bonifico_bp', __name__)

import _app 


@bonifico_bp.route('/bonifico', methods = ['GET', 'POST'])
def bonifico():
    alert = ""
    if request.method == 'POST':
        beneficiario = request.form['beneficiario']
        iban_beneficiario = request.form['iban2']
        importo = int(request.form['importo'])
        causale = request.form['causale']
        

        conto2 = _app.Conto.query.filter_by(iban = iban_beneficiario).first()
        saldo = _app.Saldo.query.filter_by(id_conto = session.get('id_conto')).first()

        if saldo.saldo_disponibile < importo:
            alert = "* IL SALDO NON SODDISFA L'IMPORTO SELEZIONATO *"

        else:
            bonifico = _app.Transazione(session.get('username'), iban_beneficiario, importo, date.today(), causale, conto2.id_conto)


            _app.db.session.add(bonifico)
            _app.db.session.commit()        
            _app.db.session.refresh(bonifico)

            update_saldo = saldo.saldo_disponibile - importo

            saldo.saldo_disponibile = update_saldo

            _app.db.session.merge(saldo)
            _app.db.session.commit()
            _app.db.session.refresh(saldo)

    return render_template('bonifico.html', session = session, alert = alert)