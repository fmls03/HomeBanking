from flask import Flask, session, Blueprint, redirect

redirecting_bp = Blueprint('redirecting_bp', __name__)

@redirecting_bp.route('/redirecting')
def redirecting():
	if not session.get('logged_in'):
		return redirect('/login')
	else:
		return redirect('/home')