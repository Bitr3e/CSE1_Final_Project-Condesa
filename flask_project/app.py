from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


@app.route("/")
def home():
    return "<h1>Hello, Flask</h1><h2><a href='/check_db'>Connection Checker</a></h2>"


@app.route("/check_db")
def check_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM mydb.customers")
        cur.close()

        return "<h2>MySQL Connection Successful!</h2>"

    except Exception as e:
        return f"<h2>MySQL Connection Failed!</h2><p>Error: {e}</p>"


if __name__ == '__main__':
    app.run(debug=True)