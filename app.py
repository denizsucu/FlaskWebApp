from flask import Flask, render_template, request, redirect, url_for, abort
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#Bootstrap işlemi

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name'] # html'deki "id" ya da "name"de geliyor
            age = form['age']
            password = generate_password_hash(form['password'])
            cur = mysql.connection.cursor() # begin
            cur.execute("INSERT INTO employee(name, age, password) VALUES(%s, %s, %s)", (name, age, password))
            mysql.connection.commit() # commit olmazsa database'e işlenmiyor
        except Exception as ex:
            return ex
    
    return render_template('index.html') # Get durumunda çalışacak bu satır

@app.route('/employees', methods=['GET'])
def employees():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM employee")

    if result > 0:
        data = cur.fetchall()
        return render_template('employees.html', employees = data)

@app.route('/dashboard/<uname>', methods=['GET'])
def dashboard(uname):
    return render_template('dashboard.html', username = uname)

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')
    

# @app.route('/login/<name>/<password>', methods=['GET','POST']) #bu şekilde name- pwd alınmaz örnek sadece
# def login(name, password):
#     if (name == 'admin' and password == 'admin'):
#         return redirect(url_for('admin'))
#     else:
#         # abort(401) #yetkisiz istek durumu
#         return redirect(url_for('register'))

@app.route('/register', methods=['GET'])
def register():
    return "This is register page"

@app.route('/admin', methods=['GET'])
def admin():
    return "This is admin dashboard"

@app.route('/static', methods=['GET'])
def static_image():
    return render_template('static.html')