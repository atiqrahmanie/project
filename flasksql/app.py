from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL



app = Flask(__name__)

# Configure the MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'
app.secret_key = 'your_secret_key'

class RegistrationForm(FlaskForm):
    # Define your form fields here
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Register")


@app.route('/register')
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data
        name = form.name.data
        Email = form.email.data
        password = form.password.data
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        # store data into db

        cursor  = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, Email,password))
        mysql.connect.commit()
        cursor.close()

        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard')

if __name__ == '__main__':
    app.run(debug=True)