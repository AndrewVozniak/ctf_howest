from flask import Flask, render_template, send_from_directory, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from faker import Faker
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin':
        return "Access Denied", 403

    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(name=data.get('username')).first()

    if not user:
        return jsonify({'message': f"User '{data.get('username')}' not found"}), 401

    if not bcrypt.check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Incorrect password'}), 401

    session['user'] = user.name
    return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/static/secret_key.zip')
def deny_secret_key():
    return "Access Denied", 403


@app.route('/logs.txt')
def logs():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'logs.txt')


@app.route('/files')
def list_files():
    files = os.listdir(os.path.join(app.root_path, 'static'))
    return jsonify(files)


@app.route('/download/<filename>')
def download_file(filename):
    print(f"User downloaded {filename}")
    return send_from_directory(os.path.join(app.root_path, 'static'), filename, as_attachment=True)


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')


def create_users():
    fake = Faker()

    print("Creating 500 users")

    for _ in range(500):
        name = fake.name()
        email = fake.email()
        password = fake.password(length=12)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if User.query.filter_by(email=email).first():
            continue

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        print(f"Created user {name} with email {email} and password {password}")

    db.session.commit()
    print("Successfully created 500 users")


if __name__ == '__main__':
    with app.app_context():
        if not User.query.filter_by(name='admin').first():
            hashed_password = bcrypt.generate_password_hash('itsaverystrongandsecretpassword').decode('utf-8')
            db.session.add(User(name='admin', password=hashed_password, email='admin@internalcrm.com'))
            db.session.commit()

        if db.session.query(User).count() <= 1:
            create_users()

    app.run(host='0.0.0.0', port=5000, debug=True)
