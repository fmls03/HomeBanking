from flask import Flask, session, Blueprint, redirect

logout_bp = Blueprint('logout_bp', __name__)


@logout_bp.route('/logout')
def logout():
	print(session)
	session.clear()
	return redirect('/')