from flask import Flask, session, Blueprint, redirect

redirecting_bp = Blueprint('redirecting_bp', __name__)

@redirecting_bp.route('/')
def redirecting():
	if session.get('logged_in') == False:
		return redirect('/login')
	else:
		return redirect('/home')