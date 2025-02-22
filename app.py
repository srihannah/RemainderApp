from flask import Flask, render_template, url_for, redirect, request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Hannah@45"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def home():
    con = mysql.connection.cursor()
    sql = 'SELECT * FROM user'  # Ensure table name is correct
    con.execute(sql)
    res = con.fetchall()
    con.close()
    return render_template('home.html', datas=res)

@app.route('/adduser', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        Company = request.form['Company']
        roll = request.form['Job']
        date = request.form['Date']
        time = request.form['Time']
        address = request.form['address']

        con = mysql.connection.cursor()
        sql = "INSERT INTO user (Company_Name,Job_Role,DateofInterview,TimeofInterview,Address) VALUES (%s, %s, %s, %s, %s)"
        con.execute(sql, (Company, roll, date, time, address))
        
        mysql.connection.commit()  # Commit using mysql.connection
        con.close()

        flash('New Interview Added')
        return redirect(url_for('home'))  # Fix function name

    return render_template('adduser.html')
@app.route('/updateuser/<string:id>', methods=['POST', 'GET'])
def Update(id):
    if request.method == 'POST':
        Company = request.form['Company']
        roll = request.form['Job']
        date = request.form['Date']
        time = request.form['Time']
        address = request.form['address']
        
        con = mysql.connection.cursor()
        sql = """UPDATE user 
                 SET Company_Name = %s, Job_Role = %s, DateofInterview = %s, 
                     TimeofInterview = %s, Address = %s 
                 WHERE ROLL_NUM = %s"""  
        
        con.execute(sql, (Company, roll, date, time, address, id))  # Fixed issue
        mysql.connection.commit()
        con.close()
        flash('Update Interview Record')
        return redirect(url_for('home'))

    con = mysql.connection.cursor()
    sql = "SELECT * FROM user WHERE ROLL_NUM = %s"
    con.execute(sql, (id,))  # Added comma to make it a tuple
    res = con.fetchone()
    
    return render_template('updateuser.html', data=res)

@app.route('/deleteuser/<string:id>', methods=['POST', 'GET'])
def Delete(id):
    con = mysql.connection.cursor()
    sql = """delete from user WHERE ROLL_NUM = %s"""  
    con.execute(sql,(id))  
    mysql.connection.commit()
    con.close()
    flash('Delete Interview Record')
    return redirect (url_for('home'))



if __name__ == "__main__":
    app.secret_key="abc123"
    app.run(debug=True)
