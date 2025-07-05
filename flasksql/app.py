from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL



app = Flask(__name__)

# Configure the MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root12345'
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secret_key'

mysql = MySQL(app)

class RegistrationForm(FlaskForm):
    # Define your form fields here
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Register")

    # for      login class
 
    class loginForm(FlaskForm):
    # Define your form fields here
   
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Register")


@app.route('/register' ,methods=['GET', 'POST'])
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
        cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, Email,password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)

@app.route('/login')
def login():
    # This is a placeholder for the login page

    form = loginForm()
    if form.validate_on_submit():
        # Process the form data
        email = form.email.data
        password = form.password.data
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        
        # store data into db
    #    we select data from user to valedate
        cursor  = mysql.connection.cursor()
        cursor.execute("SELECT *  FROM user WHERE EMAIL=%s",(email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
               session['user_id'] =user[0]

            #  password is correct
               return redirect(url_for('dashboard'))
    else:
             flash("Invalid email or password")
            # Invalid credentials
            
             return redirect(url_for('login'))
    
    return render_template('login.html',form=form)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard')

if __name__ == '__main__':
    app.run(debug=True)