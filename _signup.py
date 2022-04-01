from flask import Flask, Blueprint, redirect, render_template, request, session
from passlib.hash import sha256_crypt

from _app import *

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	return render_template('signup.html')
	