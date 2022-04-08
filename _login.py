from flask import Flask, session, render_template, redirect, request, Blueprint
from passlib.hash import sha256_crypt


login_bp = Blueprint('login_bp', __name__)

from _app import *


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
	alert = ""
	logout()
	if request.method == 'POST':
		username = request.form['username']
		passw = request.form['passw']
		users = User.query.all()
		err = 0
		for user in users:
			if username != user.username:
				err += 1
				alert = '* WRONG USERNAME *'
			elif not sha256_crypt.verify(passw, user.passw):
				err += 1
				alert = '* WRONG PASSWORD *'

		if err == 0:
			user = User.query.filter_by(username = username).first()
			conto = Conto.query.filter_by(id_user = user.id_user).first()
			session['logged_in'] = True
			session['id_user'] = user.id_user
			session['id_conto'] = conto.id_conto
			print(session.get('id_user'))
			return redirect('/redirecting')
		

	return render_template('login.html', alert = alert, session=session)