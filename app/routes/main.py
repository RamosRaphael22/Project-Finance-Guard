from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.database.connection import connect
from app import bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    connection = connect()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, password_hash, is_active, access_level, name
        FROM users
        WHERE email = %s
        """,
        (email,)
    )
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and user['is_active'] != 1:
        flash('Usuario inativo, entre em contato com o suporte.', 'danger')
        return redirect(url_for('main.index'))

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['access_level'] = user['access_level']

        return redirect(url_for('dashboard.index'))
    else:
        flash('Email ou senha inválidos.', 'danger')
        return redirect(url_for('main.index'))
