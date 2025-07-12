from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from wtforms import DateField, TimeField
import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configure the MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root12345'
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secret_key'

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




class User(UserMixin):
    def __init__(self, user_id, name,email):
        self.id = user_id
        self.name = name
        self.email = email



    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name,email FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(result[0], result[1], result[2])


class RegistrationForm(FlaskForm):
    # Define your form fields here
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Register")

    # for      login class
class loginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("login")

    # for  boarding pass form

class TravelpassForm(FlaskForm):
    name = StringField('passenger name', validators=[DataRequired()])
    passportno = StringField('passportno', validators=[DataRequired()])
    flightno = StringField('flightno', validators=[DataRequired()])
    flightfrom = StringField('flightfrom', validators=[DataRequired()])
    flightto = StringField('flightto', validators=[DataRequired()])
    date = DateField('date', format='%Y-%m-%d', default=datetime.date.today)
    time = TimeField('time', format='%H:%M' , default=datetime.datetime.now().time)

    
    submit = SubmitField('submit')

@app.route('/register' ,methods=['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit(): 
              name = form.name.data
              email = form.email.data
              password = form.password.data

              hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
 # store data into db

              cursor  = mysql.connection.cursor()
              cursor.execute("INSERT INTO user (name, email, password) values(%s, %s, %s)", (name, email, hashed_password))
              mysql.connection.commit()
              cursor.close()
              flash('Registration successful!', 'success')

              return redirect(url_for('login'))
    
        return render_template('register.html',form=form)

   
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Fetch user data from the database
         # Check if the user exists and verify the password
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name,email, password FROM user WHERE email=%s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        # If user exists and password matches
         # If user exists and password matches
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1],user_data[2])  # Assuming User class takes id, name, and password
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')   
    
    # Always return the template with the form for GET and failed POST
    return render_template('login.html' , form=form)






@app.route('/dashboard' , methods=['GET','POST'])
@login_required
def dashboard():

    form = TravelpassForm()

    if 'travel_passes' not in session:
           session['travel_passes'] = []

    passes = session['travel_passes']

    edit_index = request.args.get('edit')

    
    if request.method == 'GET' and edit_index is not None:
     if edit_index is not None:
        

        try:
                  bp = passes[int(edit_index)]
                  form.name.data = bp['name']
                  form.passportno.data = bp['passportno']
                  form.flightno.data = bp['flightno']   
                  form.flightfrom.data = bp['flightfrom'] 
                  form.flightto.data = bp['flightto']
                  form.date.data =  datetime.datetime.strptime(bp['date'] , '%Y-%m-%d').date()
                  form.time.data =  datetime.datetime.strptime(bp['time'] , '%H:%M').time()

        except (ValueError):
                    flash('Not Valid Travel pass index.')

                  
   #    submission on post

    if request.method == 'POST' and form.validate_on_submit():
        data = {
            'name': form.name.data,
            'passportno': form.passportno.data,
            'flightno': form.flightno.data,
            'flightfrom': form.flightfrom.data,
            'flightto': form.flightto.data,
            'date' : form.date.data.strftime('%Y-%m-%d'),
            'time': form.time.data.strftime('%H:%M')

            
            
        }
      

        if edit_index is not None:
               passes[int(edit_index)] = data
        
        else:
              passes.append(data)


     #    for sessions      

        session['travel_passes'] = passes
        flash('Travel pass added successfully!', 'success')
    
        return  redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, passes=passes)

   







# adding delete route


@app.route('/delete_pass/<int:index>' , methods=['POST'])

@login_required
def delete_pass(index):
    if 'travel_passes' in session:
        passes = session['travel_passes']
        if 0 <= index < len(passes):
            del passes[index]
            session['travel_passes'] = passes
            flash('Travel pass deleted successfully!', 'success')
        else:
            flash('Invalid travel pass index.', 'danger')
    else:
        flash('No travel passes found.', 'warning')
    return redirect(url_for('dashboard'))
     












@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# add home route
@app.route('/')
def home():
     return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)