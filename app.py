from flask import Flask, request, render_template_string, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "very_secure_secret_key"  # required for session

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12780377',
    'password': 'cT58Fq759x',
    'database': 'sql12780377',
    'port': 3306
}

# -------------------- LOGIN --------------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (uname, pwd))
            result = cursor.fetchone()
            if result:
                session['username'] = uname
                return redirect(url_for('dashboard'))
            else:
                message = "❌ Invalid Credentials"
        except Exception as e:
            message = "Error: " + str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template_string("""
    <html><head><title>Login</title><style>
    body { background: #f5f5f5; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .form-container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); width: 300px; }
    h2 { text-align: center; color: #333; }
    input, button { width: 100%; margin: 10px 0; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
    button { background-color: #007BFF; color: white; border: none; }
    .link { text-align: center; margin-top: 10px; }
    .msg { color: red; text-align: center; }
    </style></head><body>
    <div class="form-container">
        <h2>User Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input name="password" type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p class="msg">{{ message }}</p>
        <div class="link">Don't have an account? <a href='/register'>Register</a></div>
    </div>
    </body></html>
    """, message=message)

# -------------------- REGISTER --------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE username=%s", (uname,))
            if cursor.fetchone():
                message = "❌ Username already exists!"
            else:
                cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (uname, pwd))
                conn.commit()
                return redirect(url_for('login'))
        except Exception as e:
            message = "Error: " + str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template_string("""
    <html><head><title>Register</title><style>
    body { background: #f5f5f5; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .form-container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); width: 300px; }
    h2 { text-align: center; color: #333; }
    input, button { width: 100%; margin: 10px 0; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
    button { background-color: #28a745; color: white; border: none; }
    .link { text-align: center; margin-top: 10px; }
    .msg { color: red; text-align: center; }
    </style></head><body>
    <div class="form-container">
        <h2>User Registration</h2>
        <form method="POST">
            <input name="username" placeholder="Choose Username" required>
            <input name="password" type="password" placeholder="Choose Password" required>
            <button type="submit">Register</button>
        </form>
        <p class="msg">{{ message }}</p>
        <div class="link">Already have an account? <a href='/'>Login</a></div>
    </div>
    </body></html>
    """, message=message)

# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template_string("""
    <html><head><title>Dashboard</title><style>
    body { background-color: #e3f2fd; font-family: Arial; text-align: center; padding-top: 100px; }
    h1 { color: #007BFF; }
    </style></head><body>
        <h1>Welcome, {{ user }} 🎉</h1>
        <p>You have successfully logged in.</p>
    </body></html>
    """, user=session['username'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
