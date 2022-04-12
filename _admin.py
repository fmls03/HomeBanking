from flask import Flask, Blueprint, render_template, redirect, session

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')