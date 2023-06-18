from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import User, Customer, CombinedUser
from forms import RegistrationForm, LoginForm
from database import Database
from extensions import rows_to_dict

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db = Database('localhost', '5432', 'Orders', 'postgres', '123')
db.connect()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    users_rows = db.select(table='Customers', where_clause='user_id=%s', params=user_id)
    if users_rows:
        user = rows_to_dict(users_rows, Customer)[0]
        return Customer(company_name=user['company_name'], address=user['address'],
                        phone='phone', contact_person='contact_person')
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        # Create User and Customer objects
        user = User(username=username, password=password)
        customer = Customer(
            company_name=form.company_name.data,
            address=form.address.data,
            phone=form.phone.data,
            contact_person=form.contact_person.data
        )
        comb_user = CombinedUser(user, customer)
        query = f"CALL registrateuser('{comb_user.username}', '{comb_user.password}', '{comb_user.company_name}', " \
                f"'{comb_user.phone}', '{comb_user.address}', '{comb_user.contact_person}')"
        db.execute_query(query)
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username exists in the database
        result = db.select('users', where_clause="username = %s", params=(username,))
        if result:
            stored_password = result[0]['password_hash']

            # Check if the password is correct
            if check_password_hash(stored_password, password):
                flash('Login successful.')
                return redirect(url_for('dashboard'))

        flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
