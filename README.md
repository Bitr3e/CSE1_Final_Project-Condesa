# 🚀 CSE1 Final Project – Secure Flask Customer API  
### by *John Brence S. Condesa*

A production-ready RESTful API built with **Flask**, secured with **JWT authentication**, and integrated with a **MySQL database** to manage customer records.  
This project demonstrates industry-grade API design, secure token-based access, validation, and complete CRUD operations.

---

## 📚 Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Support and Documentation](#support-and-documentation)

---

# Project-Overview:

This API provides secure and efficient management of customer data through:y

- **JWT-protected endpoints**
- **CRUD operations for the `customers` table**
- **Error handling & response consistency**
- **Database-backed persistent storage**

---

# tech-stack:
It is built using:

| Category | Technology |
|---------|------------|
| Framework | Flask 3.1.2 |
| Database Connector | Flask-MySQLdb 2.0.0 |
| Authentication | Flask-JWT-Extended 4.7.1 |
| Driver | mysqlclient 2.2.7 |
| Language | Python 3.x |

---

# Installation:

### 1. **Prerequisites**
Ensure the following are installed:
- Python 3.6+
- MySQL Server
- pip package manager

### 2. **Clone the Repository**
```bash
git clone https://github.com/Bitr3e/CSE1_Final_Project-Condesa.git
cd CSE1_Final_Project-Condesa
```
### 3. **Create a Virtual Environment**
```bash
python -m venv venv

# Activate
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows CMD
.\venv\Scripts\Activate.ps1    # Windows PowerShell
```

### 4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 5. **Set Up the MySQL Database**
```sql
CREATE DATABASE mydb;
USE mydb;

CREATE TABLE customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL UNIQUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO customers (FirstName, LastName, Email) VALUES
('John', 'Doe', 'john.doe@example.com'),
('Jane', 'Smith', 'jane.smith@example.com'),
('Robert', 'Johnson', 'robert.johnson@example.com');
```

---

# Configuration:
Edit the database and JWT settings inside `flask_project/app.py`:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'
app.config['JWT_SECRET_KEY'] = 'super-secret-key-do-not-share'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
```
#### 🔐 Security Tips
- Use strong passwords
- Do not expose `JWT_SECRET_KEY`
- Store credentials in environment variables

---

# Running the Application:
```bash
cd flask_project
python app.py
```
#### App runs at: 
👉 http://localhost:5000/

---

# API Reference:
All endpoints except `/login` require a JWT token.

### Authorization header format:
```makefile
Authorization: Bearer <your_jwt_token>
```

---

### 1. Login – Obtain JWT Token
`POST /login`

Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
Response:
```json
{
  "access_token": "..."
}
```

---

### 2. Get All Customers
`GET /customers`

Response: 
```json
[
  {
    "CustomerID": 1,
    "FirstName": "John",
    "LastName": "Doe",
    "Email": "john.doe@example.com"
  }
]
```

---

### 3. Get Customer by ID
`GET /customers/<CustomerID>`

Response: 
```json
[
  {
    "CustomerID": 1,
    "FirstName": "John",
    "LastName": "Doe",
    "Email": "john.doe@example.com"
  }
]
```

---

### 4. Create a Customer
`POST /customers`

Body:
```json
{
  "FirstName": "Alice",
  "LastName": "Williams",
  "Email": "alice@example.com"
}
```

---

### 5. Update Customer
`PUT /customers/<CustomerID>`

Body:
```json
{
  "FirstName": "Alice",
  "LastName": "Williams",
  "Email": "alice@example.com"
}
```

---

### 6. Delete Customer
`DELETE /customers/<CustomerID>`

Response:
```json
{
  "message": "Customer ID 1 deleted successfully!"
}
```

---

### 7. Search by customer name
`GEt /customers?customer_name=brylle`

Response:
```json
{
    "CreatedAt": "Thu, 23 Oct 2025 13:08:41 GMT",
    "CustomerID": 1,
    "Email": "Cons@gmail",
    "FirstName": "Brylle",
    "LastName": "Condesa"
}
```

---

# Features:
- ✔️ JWT Authentication
- ✔️ Secure CRUD operations
- ✔️ MySQL persistent storage
- ✔️ Automatic timestamping
- ✔️ REST-standard responses
- ✔️ Detailed error handling
- ✔️ User activity logging

---

# Troubleshooting:
- **MySQL Access Denied**
Check username/password `in app.py`.
- **Token Expired**
Request a fresh token using `/login`.
- **Missing Fields**
Ensure JSON keys: `FirstName`, `LastName`, `Email`.
- **Table Not Found**
Run the SQL script in Database Setup.
- **Port in Use**
Modify:
```python
app.run(debug=True, port=5001)
```
---

# Project Structure:
```
CSE1_Final_Project-Condesa/
├── flask_project/
│   └── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Support and Documentation:
- Flask: https://flask.palletsprojects.com
- JWT Extended: https://flask-jwt-extended.readthedocs.io
- Flask-MySQLdb: https://flask-mysqldb.readthedocs.io

---

**Last Updated:** December 10, 2024  
**Repository:** https://github.com/Bitr3e/CSE1_Final_Project-Condesa  
**Version**: 1.0.0  
**Status**: ✅ Complete

---

