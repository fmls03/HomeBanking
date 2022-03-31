from flask import Flask, session, Blueprint

redirecting_bp = Blueprint('redirecting_bp', __name__)

@redirecting_bp.route('/redirecting')
def redirecting():
	if session.get('logged_in') == True:
		return redirect('/home')
	else:
		return redirect('/login')