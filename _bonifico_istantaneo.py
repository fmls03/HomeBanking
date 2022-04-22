from flask import Flask, Blueprint, render_template, request, session, redirect
import datetime
from sqlalchemy import *

bonifico_bp = Blueprint('bonifico_bp', __name__)

import _app 


@bonifico_bp.route('/bonifico', methods = ['GET', 'POST'])
def bonifico_istantaneo():
    if not session.get('logged_in'):
        return redirect('/logout')
    else:
        alert = ""
        if request.method == 'POST':
            iban_beneficiario = request.form['iban2']
            importo = int(request.form['importo'])
            causale = request.form['causale']
            
            conti = _app.Conto.query.all()
            iban_exist = 0
            
            for c in conti:
                if c.iban == iban_beneficiario:
                    iban_exist = 1
                    conto_destinatario = c

            if iban_exist == 0:
                alert = '* INSERISCI UN IBAN CORRETO *'
            else:

                conto_mittente = _app.Conto.query.filter_by(id_conto = session.get('id_conto')).first()
                if conto_mittente.saldo.saldo_disponibile < importo:
                    alert = "* IL SALDO NON SODDISFA L'IMPORTO SELEZIONATO *"
            
                elif conto_mittente.iban == iban_beneficiario:
                    alert = "* NON PUOI EFFETTUARE BONIFICI VERSO TE STESSO *"

                else:

                    bonifico = _app.Transazione(session.get('username'), iban_beneficiario, importo, datetime.datetime.now(), causale, conto_destinatario.id_conto)

                    _app.db.session.add(bonifico)
                    _app.db.session.commit()        
                    _app.db.session.refresh(bonifico)

                    # Effettuato il bonifico aggiorniamo il saldo disponibile del mittente
                    conto_mittente.saldo.saldo_disponibile -= importo + 1.50
                    conto_mittente.saldo.saldo_contabile -= importo + 1.50 

                    # Ora facciamo una select del saldo del destinatario per poi aggiornarlo con l'importo ricevuto
                    conto_destinatario.saldo.saldo_disponibile += importo
                    conto_destinatario.saldo.saldo_contabile += importo
                    

                    # applichiamo i valori modificati al database
                    _app.db.session.merge(conto_mittente)
                    _app.db.session.commit()
                    _app.db.session.refresh(conto_mittente)

                    _app.db.session.merge(conto_destinatario)
                    _app.db.session.commit()
                    _app.db.session.refresh(conto_destinatario)

                    return redirect('/home')


        return render_template('bonifico_istantaneo.html', session = session, alert = alert)