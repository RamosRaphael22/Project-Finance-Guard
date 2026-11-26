from flask import Flask
from app.database.connection import connect
from config import SYSTEM_CPF, SYSTEM_IS_ACTIVE, SYSTEM_NAME, SYSTEM_EMAIL, SYSTEM_PASSWORD, SYSTEM_ACCESS_LEVEL
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'

    bcrypt.init_app(app)

    from app.routes.main import main 
    app.register_blueprint(main)

    from app.routes.dashboard.routes import dashboard
    app.register_blueprint(dashboard) 

    create_default_admin()

    return app

def create_default_admin():
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (SYSTEM_EMAIL,)
        )

        user = cursor.fetchone()

        if user is None:
            bcrypt_password = bcrypt.generate_password_hash(SYSTEM_PASSWORD).decode('utf-8')
            cursor.execute(
                """
                INSERT INTO users SET
                    name = %s,
                    email = %s,
                    password_hash = %s,
                    access_level = %s,
                    is_active = %s,
                    cpf = %s
                """,
                (
                    SYSTEM_NAME,
                    SYSTEM_EMAIL,
                    bcrypt_password,
                    SYSTEM_ACCESS_LEVEL,
                    SYSTEM_IS_ACTIVE,
                    SYSTEM_CPF
                )
            )

            connection.commit()

    finally:
        cursor.close()
        connection.close()