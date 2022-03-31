from flask import Flask, session, Blueprint

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout')
def logout():
	session.clear()
	return redirect('/redirecting')