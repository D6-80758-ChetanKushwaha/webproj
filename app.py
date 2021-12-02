import os
from flask import Flask, app, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from datetime import timedelta
import cv2

app = Flask(__name__, template_folder='template')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.permanent_session_lifetime = timedelta(minutes=5)

UPLOAD_FOLDER = '/mnt/1C66175366172D50/Chetan Kushwaha/clg_minor_proj/Diya Patel/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST', 'GET'])
def home_page():
    if request.method == 'POST':
        f = request.files['image']
        if f:
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            return redirect(url_for('show_file', fname=fname))
    else:
        return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['login']
        session['user'] = user
        return redirect(url_for('User'))
    else:
        if 'user' in session:
            return redirect(url_for('User'))

        return render_template('login.html')


@app.route('/user')
def User():
    if "user" in session:
        user = session['user']
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/file/<fname>')
def show_file(fname):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    return render_template('show_file.html', file=full_filename)


if __name__ == "__main__":
    app.run(debug=True)
