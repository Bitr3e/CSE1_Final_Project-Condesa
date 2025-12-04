from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

app.config['JWT_SECRET_KEY'] = 'super-secret-key-do-not-share'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)


@app.route("/")
def home():
    return "<h1>Hello, Flask</h1> <br> <a href='/login'>Log-in</a>"

USERS = {
    "admin": "admin123",
    "user1": "securepass"
}

def authenticate(username, password):
    if username in USERS and USERS[username] == password:
        return True
    return False

@app.route("/login", methods=["POST"])
def login():
    """Route to issue a JWT token upon successful authentication."""
    data = request.json
    username = data.get("username", None)
    password = data.get("password", None)

    if not authenticate(username, password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    
    return jsonify(access_token=access_token)

@app.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    current_user = get_jwt_identity()
    print(f"User accessing customer list: {current_user}")

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
@jwt_required()
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



@app.route("/customers", methods=['POST'])
@jwt_required()
def create_customer():
    cur = None

    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type. Must be application/json.'}), 415

    try:
        data = request.json

        if not data or 'FirstName' not in data or 'LastName' not in data or 'Email' not in data:
            return jsonify({'error': 'Missing required fields: Firstname, Lastname, Email'}), 400
        
        customer_lastname = data['LastName']
        customer_firstname = data['FirstName']
        customer_email = data['Email']
        current_time = datetime.now()

        cur = mysql.connection.cursor()
        query = "INSERT INTO mydb.customers (FirstName, LastName, Email, CreatedAt) VALUES (%s, %s, %s, %s)"

        cur.execute(query, (customer_lastname, customer_firstname, customer_email, current_time))
        mysql.connection.commit()

        new_customer_id = cur.lastrowid

        return jsonify({
            'message': 'Customer record created successfully!',
            'CustomerID': new_customer_id,
            'First name': customer_firstname,
            'Last name': customer_lastname,
            'Email': customer_email,
            'CreatedAt': current_time 
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cur:
            cur.close()



@app.route("/customers/<int:CustomerID>", methods=['PUT'])
@jwt_required()
def update_customer(CustomerID):
    cur = None
    try:
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided for update'}), 400
        
        customer_lastname = data.get('LastName')
        customer_firstname = data.get('FirstName')
        customer_email = data.get('Email')

        updates = []
        values = []

        if customer_firstname:
            updates.append("FirstName = %s")
            values.append(customer_firstname)

        if customer_lastname:
            updates.append("LastName = %s")
            values.append(customer_lastname)
        
        if customer_email:
            updates.append("Email = %s")
            values.append(customer_email)
        
        if not updates:
            return jsonify({'m6essage': 'Missing valid fields for update'}), 400
        
        update_clause = ", ".join(updates)
        query = f"UPDATE mydb.customers SET {update_clause} WHERE CustomerID = %s"
        values.append(CustomerID)

        cur = mysql.connection.cursor()
        cur.execute(query, tuple(values))

        if cur.rowcount == 0:
            return jsonify({'message': f'Customer with ID {CustomerID} not found'}), 404
        
        mysql.connection.commit()

        return jsonify({
            'message': f'Customer ID {CustomerID} updated successfully!',
            'fields_updated': updates
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cur:
            cur.close()



@app.route("/customers/<int:CustomerID>", methods=['DELETE'])
@jwt_required()
def delete_customer(CustomerID):
    cur = None
    try:
        cur = mysql.connection.cursor()
        query = "DELETE FROM mydb.customers WHERE CustomerID = %s"
        
        cur.execute(query, (CustomerID,))
        if cur.rowcount == 0:
            return jsonify({'message': f'Customer with ID {CustomerID} not found'}), 404

        mysql.connection.commit()
        
        return jsonify({
            'message': f'Customer ID {CustomerID} deleted successfully!'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if cur:
            cur.close()



if __name__ == '__main__':
    app.run(debug=True)