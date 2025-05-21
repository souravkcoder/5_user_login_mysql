from flask import Flask, request, render_template_string, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12780377',
    'password': 'cT58Fq759x',
    'database': 'sql12780377',
    'port': 3306
}

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
            message = "✅ Login Successful!" if result else "❌ Invalid Credentials"
        except Exception as e:
            message = "Error: " + str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template_string("""
    <html><head><title>Login</title><style>
    body { font-family: Arial; margin: 40px; }
    input { margin: 5px; padding: 5px; }
    </style></head><body>
    <h2>User Login</h2>
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
    </form>
    <p>{{ message }}</p>
    <p>Don't have an account? <a href='/register'>Register here</a></p>
    </body></html>
    """, message=message)

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
    body { font-family: Arial; margin: 40px; }
    input { margin: 5px; padding: 5px; }
    </style></head><body>
    <h2>User Registration</h2>
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Register</button>
    </form>
    <p>{{ message }}</p>
    <p>Already have an account? <a href='/'>Login here</a></p>
    </body></html>
    """, message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
