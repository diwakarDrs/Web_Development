from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='template')

app.secret_key='secret123'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='crud_app'

mysql = MySQL(app)



@app.route('/')
def index():

    # Read data
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM studend_crud")
    data = curr.fetchall()
    curr.close()

    return render_template('index.html', students=data)


@app.route('/insert', methods = ['GET','POST'])
def insert():
    if request.method == "POST":

        # Create data
        flash("Data inserted successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO studend_crud(name, email, phone)VALUES (%s, %s, %s)",(name, email, phone))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST','GET'])
def update():
    if request.method =='POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()

        cur.execute("""
               UPDATE studend_crud
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
     flash('Data has been deleted successfully')
     curr= mysql.connection.cursor()
     curr.execute("DELETE FROM studend_crud WHERE id=%s",(id_data) )
     mysql.connection.commit()
     return redirect(url_for('index'))



if __name__=='__main__':
    app.run(debug=True, use_reloader=False)
