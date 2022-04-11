from flask import Flask, Blueprint, render_template, request, session
import datetime
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
        

        conto_destinatario = _app.Conto.query.filter_by(iban = iban_beneficiario).first()
        saldo_mittente = _app.Saldo.query.filter_by(id_conto = session.get('id_conto')).first()
        print(saldo_mittente.saldo_disponibile)
        if saldo_mittente.saldo_disponibile < importo:
            alert = "* IL SALDO NON SODDISFA L'IMPORTO SELEZIONATO *"

        else:
            bonifico = _app.Transazione(session.get('username'), iban_beneficiario, importo, datetime.datetime.now(), causale, conto_destinatario.id_conto)


            _app.db.session.add(bonifico)
            _app.db.session.commit()        
            _app.db.session.refresh(bonifico)

            # Effettuato il bonifico aggiorniamo il saldo disponibile del mittente
            updated_saldo_mittente = saldo_mittente.saldo_disponibile - importo
            saldo_mittente.saldo_disponibile = updated_saldo_mittente

            # Ora facciamo una select del saldo del destinatario per poi aggiornarlo con l'importo ricevuto
            saldo_destinatario = _app.Saldo.query.filter_by(id_conto = conto_destinatario.id_conto).first()
            updated_saldo_destinatario = saldo_destinatario.saldo_disponibile + importo
            saldo_destinatario.saldo_disponibile = updated_saldo_destinatario
            

            # applichiamo i valori modificati al database
            _app.db.session.merge(saldo_mittente)
            _app.db.session.commit()
            _app.db.session.refresh(saldo_mittente)

            _app.db.session.merge(saldo_destinatario)
            _app.db.session.commit()
            _app.db.session.refresh(saldo_destinatario)


    return render_template('bonifico.html', session = session, alert = alert)