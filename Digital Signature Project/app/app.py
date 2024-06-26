from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt
from functools import wraps
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import os

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', '2aa4ab0ea5ae1e6132b6bda8de7b036858761837')

app.config["MYSQL_HOST"] = os.getenv('MYSQL_HOST', 'localhost')
app.config["MYSQL_USER"] = os.getenv('MYSQL_USER', 'root')
app.config["MYSQL_PASSWORD"] = os.getenv('MYSQL_PASSWORD', 'Davide2004!')
app.config["MYSQL_DB"] = os.getenv('MYSQL_DB', 'login')

mysql = MySQL(app)

encryption_key = b"caaZ_UuXsw2DZTFhpOIP-6sWNQ5jiGl50bWKagqvUg4="
fernet = Fernet(encryption_key)

# Load the public key for verification
with open('app/keys/public_key.pem', 'rb') as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )
    
# Load your private key for signing
with open('app/keys/private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Non hai i permessi richiesti per visualizzare questa pagina.', 'danger')
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            hashed_password = account['hashed_pswd'].encode('utf-8')
            salt = account['salt'].encode('utf-8')
            if bcrypt.hashpw(password, salt) == hashed_password:
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = account["username"]
                session["is_admin"] = account["is_admin"]
                session["email"] = account["email"]
                msg = "Login effettuato correttamente!"
                return redirect(url_for("upload"))
            else:
                msg = "Username o password errata!"
        else:
            msg = "Username o password errata!"
    return render_template("login.html", msg=msg)

@app.route("/upload")
@login_required
def upload():
    return render_template('upload.html')

@app.route('/verify')
@login_required
def verify():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, title FROM documents WHERE id_account = %s", (session['id'],))
    files = cursor.fetchall()
    msg = request.args.get('msg', '')
    return render_template('verify.html', files=files, msg=msg)

@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html')

@app.route("/logout")
@login_required
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form and "email" in request.form:
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        email = request.form["email"]
        consent = 'consent' in request.form

        if not consent:
            msg = "Devi prima accettare le norme sulla privacy."
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
            account = cursor.fetchone()
            if account:
                msg = "Account, già esistente, usare un altro username."
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                msg = "e-mail non valida."
            elif not re.match(r"[A-Za-z0-9]+", username):
                msg = "L'username deve contenere solo numeri e caratteri!"
            elif not username or not password or not email:
                msg = "Per favore riemi tutti i campi."
            else:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password, salt)
                cursor.execute(
                    "INSERT INTO accounts (username, hashed_pswd, salt, email) VALUES (%s, %s, %s, %s)",
                    (username, hashed_password.decode('utf-8'), salt.decode('utf-8'), email),
                )
                mysql.connection.commit()
                msg = "Registrazione terminata con successo!"
    elif request.method == "POST":
        msg = "Per favore riemi tutti i campi."
    return render_template("register.html", msg=msg)

@app.route('/uploadfile', methods=['GET', 'POST'])
@login_required
def uploadfile():
    msg = ''
    if request.method == 'POST' and 'file' in request.files and 'title' in request.form:
        file = request.files['file']
        title = request.form['title']
        if file and title:
            content = file.read()
            encrypted_content = fernet.encrypt(content)

            # Generate digital signature
            signature = private_key.sign(
                content,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "INSERT INTO documents (title, hashed_content, id_account, digital_sign) VALUES (%s, %s, %s, %s)",
                (title, encrypted_content, session['id'], signature)
            )
            mysql.connection.commit()
            msg = 'File salvato correttamente!'
        else:
            msg = 'Per favore inserisci sia il titolo che il file da salvare.'
    return render_template('upload.html', msg=msg)

@app.route('/myfiles')
@login_required
def myfiles():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, title FROM documents WHERE id_account = %s", (session['id'],))
    files = cursor.fetchall()
    return render_template('myfiles.html', files=files)

@app.route('/download/<int:file_id>')
@login_required
def download(file_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT title, hashed_content FROM documents WHERE id = %s AND id_account = %s", (file_id, session['id']))
    file = cursor.fetchone()
    if file:
        decrypted_content = fernet.decrypt(file['hashed_content'])
        response = make_response(decrypted_content)
        response.headers['Content-Disposition'] = f'attachment; filename={file["title"]}'
        response.mimetype = 'application/octet-stream'
        return response
    else:
        return 'File non trovato o accesso non consentito', 404

@app.route('/delete/<int:file_id>')
@login_required
def delete(file_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "DELETE FROM documents WHERE id=%s AND id_account=%s;"
    args = (file_id, session['id'])
    cursor.execute(query, args)
    msg = 'File eliminato con successo'
    mysql.connection.commit()
    return redirect(url_for('myfiles', msg=msg))

@app.route('/deleteaccount', methods=['POST'])
@login_required
def deleteaccount():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "DELETE FROM accounts WHERE id = %s;"
    args = (session['id'],)
    cursor.execute(query, args)
    mysql.connection.commit()
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route('/makeadmin', methods=['POST'])
@admin_required
def makeadmin():
    data = request.get_json()
    account_id = data.get('account_id')
    if account_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET is_admin = 1 WHERE id = %s", (account_id,))
        mysql.connection.commit()
        return '', 200
    return '', 400

@app.route('/removeadmin', methods=['POST'])
@admin_required
def removeadmin():
    data = request.get_json()
    account_id = data.get('account_id')
    if account_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET is_admin = 0 WHERE id = %s", (account_id,))
        mysql.connection.commit()
        return '', 200
    return '', 400

@app.route('/delete_user_account', methods=['POST'])
@admin_required
def delete_user_account():
    data = request.get_json()
    account_id = data.get('account_id')
    if account_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
        mysql.connection.commit()
        return '', 200
    return '', 400

@app.route('/verifyfile', methods=['POST'])
@login_required
def verifyfile():
    msg = ''
    if request.method == 'POST' and 'file' in request.files:
        user_file = request.files['file']
        content = user_file.read()
        file_id = request.form['document_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT hashed_content, digital_sign FROM documents WHERE id = %s AND id_account = %s", (file_id, session['id']))
        file = cursor.fetchone()

        if file:
            try:
                # Decrittazione del contenuto del file
                decrypted_content = fernet.decrypt(file['hashed_content'])

                try:
                    # Verifica della firma digitale
                    public_key.verify(
                        file['digital_sign'],
                        decrypted_content,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    if content == decrypted_content:
                        msg = 'Il file è valido e la firma digitale è corretta.'
                    else:
                        msg = 'Il file è corrotto.'
                except Exception as e:
                    msg = 'Firma digitale non valida.'
            except Exception as e:
                msg = 'Errore imprevisto: {}'.format(str(e))
        else:
            msg = 'File non trovato oppure invalido.'
    else:
        msg = 'Nessun file inserito.'
    return redirect(url_for('verify', msg=msg))

@app.route("/pagina_admin")
@admin_required
def pagina_admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    return render_template('users.html', accounts=accounts)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == "__main__":
    app.run(debug=True)
