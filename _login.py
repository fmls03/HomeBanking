from flask import Flask, session, render_template, redirect, request, Blueprint
from passlib.hash import sha256_crypt


login_bp = Blueprint('login_bp', __name__)

from _app import *


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
	alert = ""
	err = 0
	logout()
	if request.method == 'POST':
		username = request.form['username']
		passw = request.form['passw']
		users = User.query.all()
		for user in users:
			if username == user.username:
				if passw == sha256_crypt.verify(passw, user.passw):
					session['logged_in'] = True
					return redirect('/')				
				else:
					err += 1
			else:
				err += 1

		if err > 0:
			alert = '* WRONG CREDENTIALS *'

	return render_template('login.html', alert = alert)