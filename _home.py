from flask import  Blueprint, render_template, session

home_bp = Blueprint('home_bp', __name__)

from _app import *

@home_bp.route('/home')
def home():
    if session.get('logged_in') == False:
        return redirect('/')
    return render_template('home.html')
    
