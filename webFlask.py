import os
from flask import Flask, render_template, request, redirect
import sqlite3
import logging  #*Import the logging module

app = Flask(__name__, static_url_path='/static')

#*Implementing logging 
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

#*Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

#set up SQLite databse connection 
DATABASE = "mydatabase.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return  conn, conn.cursor() # OJO AGREGO , conn.cursor()

@app.route("/")
def index():
    #tomar la data de la base 
    conn, cursor = get_db_connection() # OJO AGREGO CURSOR
    tutorialesImportantes = cursor.execute('SELECT * FROM tutorialesImportantes').fetchall()  # OJO QUITE conn.execute Y COLOCO cursor.execute
    conn.close()
    #render the template with the data 
    return render_template('index.html', tutorialesImportantes=tutorialesImportantes)

@app.route('/add_tutoriales', methods=['POST']) #'GET' ,
def add_tutoriales():
    #retrive from database
    title = request.form['title']
    author = request.form['author']
    url   = request.form['url']
    visto = request.form['visto']
    year = request.form['year']#.get
    
    #insertando los datos a la base
    conn, cursor = get_db_connection()
    cursor.execute('INSERT INTO tutorialesImportantes(title, author, url, visto, year) VALUES (?,?,?,?,?)',
                   (title, author, url, visto, year)) # OJO QUITE conn.execute COLOCO cursor.execute
    conn.commit()
    conn.close()
    
    # Log the addition of a tutorial
    logging.info(f"Added tutorial: {title} by {author}")
    
    #lo regirige a la pagina principal 
    return redirect('/')

@app.route('/list')
def list_tutorials():
   conn, cursor = get_db_connection()#.connect  OJO LO CORTE AQUI , quito esto como parametro "database.db"
   rows = cursor.execute('SELECT * FROM tutorialesImportantes').fetchall()
   conn.close()
   return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)



