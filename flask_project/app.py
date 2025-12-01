from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

def check_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM mydb.customers")
        cur.close()

        return "<h2>MySQL Connection Successful!</h2>"

    except Exception as e:
        return f"<h2>MySQL Connection Failed!</h2><p>Error: {e}</p>"
    

@app.route("/")
def home():
    return "<h1>Hello, Flask</h1>"


@app.route('/customers', methods=['GET'])
def get_customers():
    try: 
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM mydb.customers")

        if result > 0:
            customer_details = cur.fetchall()
            column_names = [i[0] for i in cur.description]

            customer_list = []
            for row in customer_details:
                customer_list.append(dict(zip(column_names, row)))

            cur.close()

            return jsonify(customer_list)
        else:
            cur.close()
            return jsonify({'message': 'No customers found'}), 404
        
    except Exception as  e:
        print(f"Database Error: {e}")
        return jsonify({'error': 'An internal error occured'}), 500
    

@app.route("/customers/<int:CustomerID>", methods=['GET'])
def get_customer(CustomerID):
    cur = None
    try:
        cur = mysql.connection.cursor()
        sql_query = "SELECT * FROM mydb.customers WHERE CustomerID = %s"

        resultValue = cur.execute(sql_query, (CustomerID,))

        if resultValue > 0:
            customer_data = cur.fetchone()
            column_names = [i[0] for i in cur.description]
            customer_dict = dict(zip(column_names, customer_data))

            return jsonify(customer_dict)
        
        else:
            return jsonify({'message': f'Customer with ID {CustomerID} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cur:
            cur.close()

if __name__ == '__main__':
    app.run(debug=True)