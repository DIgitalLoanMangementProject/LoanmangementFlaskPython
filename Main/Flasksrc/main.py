from flask import render_template, redirect, url_for, flash
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from sqlalchemy.orm import Session

from Flasksrc.importloans import loanapplier

 
 
# Create a flask application
app = Flask(__name__, template_folder='../html')
app.config['SECRET_KEY'] = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:adminPass@localhost:3306/loan_management_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from functools import wraps
from flask import abort
from flask_login import current_user

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'customer':
            if current_user.is_authenticated :
                flash(f"Already loged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name} Not access employee/admin pages")
                if current_user.user_type == "customer":
                    return redirect(url_for('Customerindex'))
                elif current_user.user_type == "employee":
                    return redirect(url_for('Employeeindex'))
                elif current_user.user_type == "admin":
                    return redirect(url_for('Adminindex'))
            abort(403)  # Unauthorized
        return f(*args, **kwargs)
    return decorated_function

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'employee':
            if current_user.is_authenticated :
                flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name} Not access customer/admin pages")
                if current_user.user_type == "customer":
                    return redirect(url_for('Customerindex'))
                elif current_user.user_type == "employee":
                    return redirect(url_for('Employeeindex'))
                elif current_user.user_type == "admin":
                    return redirect(url_for('Adminindex'))
            abort(403)  # Unauthorized
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            if current_user.is_authenticated :
                flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name} Not access employee/customer pages")
                if current_user.user_type == "customer":
                    return redirect(url_for('Customerindex'))
                elif current_user.user_type == "employee":
                    return redirect(url_for('Employeeindex'))
                elif current_user.user_type == "admin":
                    return redirect(url_for('Adminindex'))
            abort(403)  # Unauthorized
        return f(*args, **kwargs)
    return decorated_function


# Create user model



class Bank(db.Model):
    __tablename__ = 'bank'
    bankID = db.Column(db.String(255), primary_key=True)
    bankName = db.Column(db.String(255))
    address = db.Column(db.String(255))
    mobileno = db.Column(db.String(20))
    email_adress = db.Column(db.String(255))
    # Relationships
    employees = db.relationship('Employee', backref='bank')
    loan_details = db.relationship('LoanDetails', backref='bank')
    loan_types = db.relationship('LoanType', backref='bank')



from abc import ABC, abstractmethod

class Observable():
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

class EmployeeObserver():
    @abstractmethod
    def update(self, message):
        pass


class Employee(db.Model,UserMixin,EmployeeObserver):
    __tablename__ = 'employee'
    empID = db.Column(db.String(255), primary_key=True)
    empName = db.Column(db.String(255))
    empAddress = db.Column(db.String(255))
    emailaddress = db.Column(db.String(255))
    bankID = db.Column(db.String(255), db.ForeignKey('bank.bankID'))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def update(self, message):
        # Handle the notification received from Observable
        # For example, save notification to employee.csv
        with open(f'{self.empID}employee.txt', 'a') as file:
            file.write(f"employee object log: {message}\n")


class CustomerObserver():
    @abstractmethod
    def update(self, message):
        pass
class Customer(db.Model,UserMixin):
    __tablename__ = 'customer'
    customerID = db.Column(db.String(255), primary_key=True)
    customerName = db.Column(db.String(255))
    mobileno = db.Column(db.String(20))
    address = db.Column(db.String(255))
    emailaddress = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    loan_details = db.relationship('LoanDetails', backref='customer')

    def get_id(self):
        return self.customerID

    def update(self, message):
        # Handle the notification received from Observable
        # For example, save notification to customer.csv
        with open(f'{self.customerID}customer.csv', 'a') as file:
            file.write(f"cusomer object log :{message}\n")

@login_manager.user_loader
def loader_user(user_id):
    return AllUserTable.query.get(user_id)
    # with db.session.begin():
    #     return Session(db.session).get(Customer, user_id)
class Observable:
    _observers=[]
    @classmethod
    def add_observer(cls, observer):
        cls._observers.append(observer)

    @classmethod
    def remove_observer(cls, observer):
        cls._observers.remove(observer)

    @classmethod
    def notify_observers(cls, message):
        for ob in cls._observers:
            ob.update(message)

    # @classmethod
    # def notify(cls,message)

class LoanDetails(db.Model):
    __tablename__ = 'loan_details'
    applicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerID = db.Column(db.String(255), db.ForeignKey('customer.customerID'))
    loanType = db.Column(db.String(255))
    bankID = db.Column(db.String(255), db.ForeignKey('bank.bankID'))
    interest = db.Column(db.DECIMAL(5, 2))
    loanStatus = db.Column(db.String(50))
    amount = db.Column(db.DECIMAL(10, 2))

    def __init__(self, *args, **kwargs):
        super(LoanDetails, self).__init__(*args, **kwargs)
        self._observers = []
    
    # def add_observer(self, observer):
    #     self._observers.append(observer)

    # def remove_observer(self, observer):
    #     self._observers.remove(observer)

    # def notify_observers(self, message):
    #     for observer in self._observers:
    #         observer.update(message)
    # Relationship with Customer
    # customer = db.relationship('Customer', backref='loan_details')

    # Rename the backref for Bank
    # bank_details = db.relationship('Bank', backref='loan_details')
    @classmethod
    def update_status(cls, new_status):
        message = f"Status updated to {new_status}"
        Observable.notify_observers( message)

class LoanType(db.Model):
    __tablename__ = 'loantypes'
    loanTypeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bankID = db.Column(db.String(255), db.ForeignKey('bank.bankID'))
    loanType = db.Column(db.String(255))
    interestRate = db.Column(db.DECIMAL(5, 2))
    # bank = db.relationship('Bank', backref=db.backref('loan_types', lazy='dynamic'))

class AdminTable(db.Model,UserMixin):
    __tablename__ = 'admin'
    adminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


from datetime import datetime

class LoanStatusChangesObserver:
    def __init__(self, filename):
        self.filename = filename

    def update(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: {message}"
        with open(self.filename, 'a') as file:
            file.write(log_entry + '\n')

loan_status_observer = LoanStatusChangesObserver('loan_status_log.txt')

Observable.add_observer(loan_status_observer)

""" class ExistingTable(db.Model):
    __tablename__ = 'existing_table_name'  # Match the table name in your existing DB

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Define other columns to match the existing table schema
    # ... """
 


class CustomerLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EmployeeLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    submit = SubmitField('Login')

class AllUserTable(db.Model,UserMixin):
    __tablename__ = 'all_user_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    user_id_online = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return self.id

def customerlogin(username, password):
    customer = Customer.query.filter_by(username=username, password=password).first()
    if customer:
        # User found
        return customer #.customerID, customer.username
    else:
        # User not found
        return None

def login(username, password, usertype):
    if usertype == "customer":
        customer = Customer.query.filter_by(username=username, password=password).first()
        if customer:
            customer_id = customer.customerID
            user_from_all_users = AllUserTable.query.filter_by(user_type='customer', user_id_online=customer_id).first()
            if user_from_all_users:
                print("User found in AllUserTable")
                return user_from_all_users
            else:
                # If user not found in AllUserTable, create a new entry
                new_user = AllUserTable(name=username, password=password, user_type='customer', user_id_online=customer_id)
                db.session.add(new_user)
                db.session.commit()
                print("New user added to AllUserTable")
                return new_user
        else:
            print("Customer not found")
            return None

    elif usertype == "employee":
        employee = Employee.query.filter_by(username=username, password=password).first()
        if employee:
            employee_id = employee.empID
            user_from_all_users = AllUserTable.query.filter_by(user_type='employee', user_id_online=employee_id).first()
            if user_from_all_users:
                print("User found in AllUserTable")
                return user_from_all_users
            else:
                new_user = AllUserTable(name=username, password=password, user_type='employee', user_id_online=employee_id)
                db.session.add(new_user)
                db.session.commit()
                print("New user added to AllUserTable")
                return new_user
        else:
            print("Employee not found")
            return None

    elif usertype == "admin":
        admin = AdminTable.query.filter_by(username=username, password=password).first()
        if admin:
            admin_id = admin.adminID
            user_from_all_users = AllUserTable.query.filter_by(user_type='admin', user_id_online=admin_id).first()
            if user_from_all_users:
                print("User found in AllUserTable")
                return user_from_all_users
            else:
                new_user = AllUserTable(name=username, password=password, user_type='admin', user_id_online=admin_id)
                db.session.add(new_user)
                db.session.commit()
                print("New user added to AllUserTable")
                return new_user
        else:
            print("admin not found")
            return None

    return None




login_manager.login_view = 'CustomerLogin'

@app.route('/', methods=["GET", "POST"])
@app.route('/CustomerLogin', methods=["GET", "POST"])
def CustomerLogin():
    if current_user.is_authenticated :
        flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name}")
        if current_user.user_type == "customer":
            return redirect(url_for('Customerindex'))
        elif current_user.user_type == "employee":
            return redirect(url_for('Employeeindex'))
        elif current_user.user_type == "admin":
            return redirect(url_for('Adminindex'))
    form = CustomerLoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        username = form.username.data
        password = form.password.data
        customer:Customer = customerlogin(username,password)
        if customer:
            print(customer.customerID," customer id")
            loguser=login(username,password,"customer")
            login_user(loguser)
            flash(f"logged in as {username}")
            return redirect(url_for('Customerindex'))
        print("login failed")
        flash('Invalid username or password')
    # Renders sign_up template if user made a GET request
    return render_template("CustomerLogin.html", form=form)

class CustomerRegistrationForm(FlaskForm):
    customer_id = StringField('Customer ID',render_kw={'readonly': True})
    customer_name = StringField('Customer Name')
    address = StringField('Address')
    email_address = StringField('Email Address')
    mobile_no = StringField('Mobile Number')
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Register')

@app.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if current_user.is_authenticated :
        flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name}")
        if current_user.user_type == "customer":
            return redirect(url_for('Customerindex'))
        elif current_user.user_type == "employee":
            return redirect(url_for('Employeeindex'))
        elif current_user.user_type == "admin":
            return redirect(url_for('Adminindex'))
    form = CustomerRegistrationForm()
    max_customer_id = db.session.query(db.func.max(Customer.customerID)).scalar()

    if form.validate_on_submit():
        # Process the form data (e.g., save to database)
        customer_id = int(form.customer_id.data)
        customer_name = form.customer_name.data
        address = form.address.data
        email_address = form.email_address.data
        mobile_no = form.mobile_no.data
        username = form.username.data
        password = form.password.data

        # Perform database operations or other actions with the form data
        new_customer = Customer(
            customerID=customer_id,
            customerName=customer_name,
            mobileno=mobile_no,
            address=address,
            emailaddress=email_address,
            username=username,
            password=password
        )
        db.session.add(new_customer)
        db.session.commit()

        # For AllUserTable, assuming you want to store the user as 'customer'
        new_user = AllUserTable(
            name=username,
            password=password,
            user_type='customer',
            user_id_online=customer_id
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Registration Successfull and loogedd in as {username}")

        # Redirect to a success page or home page after registration
        return redirect(url_for('Customerindex'))
    form.customer_id.data=str(int(max_customer_id)+1)

    return render_template('CustomerRegister.html', form=form)

@app.route('/loanapplications')
def loanapplications():
    # Fetch available loans by joining LoanType with Bank
    available_loans = db.session.query(LoanType, Bank).join(Bank).all()

    return render_template('loan_applications.html', available_loans=available_loans)


def employeelogin(username, password):
    employee = Employee.query.filter_by(username=username, password=password).first()
    if employee:
        # User found
        return employee
    else:
        # User not found
        return None


@app.route('/EmployeeLogin', methods=["GET", "POST"])
def EmployeeLogin():
    if current_user.is_authenticated :
        flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name}")
        if current_user.user_type == "customer":
            return redirect(url_for('Customerindex'))
        elif current_user.user_type == "employee":
            return redirect(url_for('Employeeindex'))
        elif current_user.user_type == "admin":
            return redirect(url_for('Adminindex'))
    form = EmployeeLoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        username = form.username.data
        password = form.password.data
        employee = employeelogin(username, password)
        if employee:
            loguser = login(username, password, "employee")
            login_user(loguser)
            flash(f"logged in as {username}")
            return redirect(url_for('Employeeindex'))
        flash('Invalid username or password')
    return render_template("EmployeeLogin.html", form=form)


def adminlogin(username, password):
    admin = AdminTable.query.filter_by(username=username, password=password).first()
    if admin:
        # User found
        return admin
    else:
        # User not found
        return None

@app.route('/AdminLogin', methods=["GET", "POST"])
def AdminLogin():
    if current_user.is_authenticated :
        flash(f"Already looged in {current_user.user_type} [{current_user.user_id_online}] {current_user.name}")
        if current_user.user_type == "customer":
            return redirect(url_for('Customerindex'))
        elif current_user.user_type == "employee":
            return redirect(url_for('Employeeindex'))
        elif current_user.user_type == "admin":
            return redirect(url_for('Adminindex'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        username = form.username.data
        password = form.password.data
        admin = adminlogin(username, password)
        if admin:
            loguser = login(username, password, "admin")
            login_user(loguser)
            flash(f"logged in as {username}")
            return redirect(url_for('Adminindex'))
        flash('Invalid username or password')
    return render_template("AdminLogin.html", form=form)

@app.route('/logout')
@login_required  # Protect this route to ensure only logged-in users can log out
def logout():
    logout_user()
    # Redirect to the home page or any other desired page after logout
    return redirect(url_for('CustomerLogin'))  # Replace 'index' with your desired endpoint


@app.route('/Customerindex', methods=["GET", "POST"])
@login_required
@customer_required
def Customerindex():
    customer_id = current_user.user_id_online
    user_loan_details = db.session.query(LoanDetails, Bank.bankName).\
        join(Bank, LoanDetails.bankID == Bank.bankID).\
        filter(LoanDetails.customerID == customer_id).all()
    return render_template("CustomerHome.html", user_loan_details=user_loan_details)

@app.route('/Employeeindex', methods=["GET", "POST"])
@login_required
@employee_required
def Employeeindex():
    # Get employee details along with related bank details
    employee = Employee.query.filter_by(empID=current_user.user_id_online).first()
    if employee:
        bank = Bank.query.filter_by(bankID=employee.bankID).first()
        loan_applications = (
        LoanDetails.query
        .join(Customer, LoanDetails.customerID == Customer.customerID)
        .join(Bank, LoanDetails.bankID == Bank.bankID)
        .all()
    )
        return render_template("EmployeeHome.html", employee=employee, bank=bank,loan_applications=loan_applications)
    else:
        # Handle the case where employee details are not found
        return render_template("EmployeeNotFound.html")

class LoanTypeCreateForm(FlaskForm):
    loan_type = StringField('Loan Type', validators=[DataRequired()])
    interest_rate = DecimalField('Interest Rate', validators=[DataRequired()])
    # max_amount = DecimalField('Maximum Amount', validators=[DataRequired()])
    bank = QuerySelectField('Bank', query_factory=lambda: Bank.query.all(), get_label='bankName')
    submit = SubmitField('Create Loan Type')

@app.route('/create_loan_type', methods=['GET', 'POST'])
@login_required
@employee_required
def create_loan_type():
    form = LoanTypeCreateForm()
    
    if form.validate_on_submit():
        # Access form data
        loan_type = form.loan_type.data
        interest_rate = form.interest_rate.data
        # max_amount = form.max_amount.data
        
        selected_bank = form.bank.data  # Get the selected bank from the form
        
        # Perform the necessary actions to add a new loan type using the form data
        if selected_bank:
            new_loan_type = LoanType(
                loanType=loan_type,
                interestRate=interest_rate,
                # maxAmount=max_amount,
                bankID=selected_bank.bankID  # Assign the selected bank's ID to the loan type
            )
            db.session.add(new_loan_type)
            db.session.commit()
            flash("Loan type created successfully")
            return redirect(url_for('Employeeindex'))  # Redirect to employee dashboard or any other route
        else:
            flash("Failed to create loan type. Please select a bank.")
        flash("Failed to create loan type")
        
    return render_template('loan_type_create.html', form=form)

@app.route('/editstatus/<int:loan_application_id>', methods=['GET', 'POST'])
@login_required
@employee_required
def edit_loan_application_status(loan_application_id):
    loan_application_details = LoanDetails.query.filter_by(applicationID=loan_application_id).first()
    bank = Bank.query.filter_by(bankID=loan_application_details.bankID).first()
    customer=Customer.query.filter_by(customerID=loan_application_details.customerID).first()

    if not loan_application_details:
        # Handle case where loan application ID does not exist
        return render_template('error_page.html', message='Loan application not found')

    form = LoanApplicationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Update loan status in the database
            old_status = loan_application_details.loanStatus
            new_loan_status = form.loan_status.data
            loan_application_details.loanStatus = new_loan_status

            # Commit changes to the database
            db.session.commit()
            flash(f"{loan_application_id} status updated from {old_status} to  '{new_loan_status}' ")
            employee = Employee.query.filter_by(empID=current_user.user_id_online).first()
            status_log_message = f"Loan application {loan_application_id} status updated from {old_status} to '{new_loan_status}' by Employee {employee.empID}"
            loan_application_details.update_status(status_log_message)

            # Redirect to another route or display a success message upon successful update
            return redirect(url_for('Employeeindex'))

    # Populate form fields with loan application details
    form.customer_name.data = customer.customerName# Replace with actual customer details
    form.loan_type.data = loan_application_details.loanType
    form.bank_name.data = bank.bankName  # Replace with actual bank details
    form.interest.data = loan_application_details.interest
    form.loan_status.data = loan_application_details.loanStatus
    form.amount.data = loan_application_details.amount

    return render_template('editLoanStatus.html', form=form)
class LoanApplicationForm(FlaskForm):
    customer_name = StringField('Customer Name')
    loan_type = StringField('Loan Type')
    bank_name = StringField('Bank Name')
    interest = DecimalField('Interest Rate')
    loan_status = StringField('Loan Status', validators=[DataRequired()])
    amount = DecimalField('Amount')
    submit = SubmitField('Submit')

class LoanApplicationForm2(FlaskForm):
    customer_name = StringField('Customer Name',render_kw={'readonly': True})
    loan_type = StringField('Loan Type',render_kw={'readonly': True})
    bank_name = StringField('Bank Name',render_kw={'readonly': True})
    interest = DecimalField('Interest Rate',render_kw={'readonly': True})
    loan_status = StringField('Loan Status', validators=[DataRequired()],render_kw={'readonly': True})
    amount = DecimalField('Amount')
    submit = SubmitField('Submit')


""" 

class LoanType(db.Model):
    __tablename__ = 'loantypes'
    loanTypeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bankID = db.Column(db.String(255), db.ForeignKey('bank.bankID'))
    loanType = db.Column(db.String(255))
    interestRate = db.Column(db.DECIMAL(5, 2))
    bank = db.relationship('Bank', backref=db.backref('loan_types', lazy='dynamic'))

 """

@app.route('/apply/<int:loan_type_id>', methods=['GET', 'POST'])
@login_required
@customer_required
def apply_loan(loan_type_id):
    form = LoanApplicationForm()
    loan_type = LoanType.query.get(loan_type_id)

    if form.validate_on_submit():
        # Assuming 'customerID' comes from the currently logged-in user
        # new_loan = LoanDetails(
        #     customerID=current_user.user_id_online,
        #     loanType=loan_type_id,  # Assuming loan type ID is passed through the URL
        #     bankID=loan_type.bank.bankID,  # Assuming bank ID is part of the form
        #     interest=loan_type.interestRate,  # Assuming interest is part of the form
        #     loanStatus=form.loan_status.data,  # Assuming a new loan application starts with 'Pending' status
        #     amount=form.amount.data,
        # )

        loanapplier.set_strategy(loan_type.loanType)  # Set the loan type strategy
        loanapplier.apply_loan(
            customer_id=current_user.user_id_online,
            bank_id=loan_type.bank.bankID,
            amount=form.amount.data
        )

        # Save the new loan application to the database
        # db.session.add(new_loan)
        
        db.session.commit()

        flash('Loan application submitted successfully!', 'success')
        return redirect(url_for('Customerindex'))  # Redirect to loan applications page
    # fill defaults except amount
    else:
        
        if loan_type:
            # If the loan type is found, set form fields with values from this loan type
            # For instance, if your LoanTypeModel contains a field for default interest, you can set it like this:
            form.interest.data = loan_type.interestRate  # Assuming 'default_interest' is a field in your model
            form.customer_name.data= current_user.name
            form.loan_type.data = loan_type.loanType
            #bank = Bank.query.filter_by(bankID=loan_type.bankID).first()
            form.bank_name.data= loan_type.bank.bankName
            form.loan_status.data = "Application Intial Process draft"

        return render_template('apply_loan.html', form=form)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BankCreateForm(FlaskForm):
    bankID = StringField('Bank ID', validators=[DataRequired()],render_kw={'readonly': True})
    bankName = StringField('Bank Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    mobileno = StringField('Mobile Number', validators=[DataRequired()])
    email_adress = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    empID = StringField('Employee ID', validators=[DataRequired()],render_kw={'readonly': True})
    empName = StringField('Employee Name', validators=[DataRequired()])
    empAddress = StringField('Address', validators=[DataRequired()])
    emailaddress = StringField('Email Address', validators=[DataRequired()])
    bank = QuerySelectField(query_factory=lambda: Bank.query.all(), get_label='bankName', allow_blank=True)
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Employee')


@app.route('/Adminindex', methods=["GET", "POST"])
@login_required
@admin_required
def Adminindex():
    bankCreateform = BankCreateForm()
    employeeCreateForm = EmployeeForm()
    banks = Bank.query.all() 
    max_bank_id = db.session.query(db.func.max(Bank.bankID)).scalar()
    bankCreateform.bankID.data = int(max_bank_id)+1
    max_emp_id = db.session.query(db.func.max(Employee.empID)).scalar()
    employeeCreateForm.empID.data = int(max_emp_id)+1
    emps = Employee.query.all() 
    return render_template("AdminHome.html",bankCreateform=bankCreateform,banks=banks,employee_form=employeeCreateForm,emps=emps)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    
    if form.validate_on_submit() and form.bank.data:
        new_employee = Employee(
            empID=form.empID.data,
            empName=form.empName.data,
            empAddress=form.empAddress.data,
            emailaddress=form.emailaddress.data,
            bankID=form.bank.data.bankID if form.bank.data else None,
            username=form.username.data,
            password=form.password.data
        )

        db.session.add(new_employee)
        db.session.commit()
        flash(f"Added Employee Emp ID {form.empID.data}")
    else:
        flash("Failed to add Employee")
    return redirect(url_for('Adminindex'))


@app.route('/add_bank', methods=['POST'])
@login_required
@admin_required
def add_bank():
    form = BankCreateForm(request.form)
    
    if form.validate():
        # Access form data
        bank_id = form.bankID.data
        bank_name = form.bankName.data
        address = form.address.data
        mobile_no = form.mobileno.data
        email_adress = form.email_adress.data
        
        # Perform the necessary actions to add a new bank using the form data
        # You can use the provided bankid from the route and/or the form data to add the bank
        
        # Example: Adding a new bank to the database
        new_bank = Bank(
            bankID=bank_id,
            bankName=bank_name,
            address=address,
            mobileno=mobile_no,
            email_adress=email_adress
        )
        db.session.add(new_bank)
        db.session.commit()
        flash("Bank added successfully")
        
        # Redirect to the admin index route after adding the bank
        
    else:
        # Handle form validation errors
        flash( "Form validation failed. Please check your inputs. bank not added")
    return redirect(url_for('Adminindex'))

@app.route('/delete/<bankid>', methods=['GET'])
@login_required
@admin_required
def delete_bank(bankid):
    # Find the bank by ID
    bank_to_delete = Bank.query.filter_by(bankID=bankid).first()

    if bank_to_delete:
        # If the bank exists, delete it from the database
        db.session.delete(bank_to_delete)
        db.session.commit()
        flash(f"Bank with ID {bankid} has been deleted successfully.")
    else:
        flash(f"Bank with ID {bankid} not found.")
    return redirect(url_for('Adminindex'))


@app.route('/delete_emp/<empID>', methods=['GET'])
@login_required
@admin_required
def delete_emp(empID):
    emp_to_delete = Employee.query.filter_by(empID=empID).first()

    if emp_to_delete:
        # If the bank exists, delete it from the database
        db.session.delete(emp_to_delete)
        db.session.commit()
        flash(f"Employee with ID {empID} has been deleted successfully.")
    else:
        flash(f"Employee with ID {empID} not found.")
    return redirect(url_for('Adminindex'))

from flask import render_template, redirect, url_for

# Route to render the update bank details form
@app.route('/update_bank/<bank_id>', methods=['GET'])
@login_required
@admin_required
def render_update_bank_form(bank_id):
    bank = Bank.query.filter_by(bankID=bank_id).first()
    if bank:
        # Pass the bank details to the HTML form
        return render_template('update_bank.html', bankCreateform=BankCreateForm(obj=bank), bank=bank)
    else:
        flash(f"Bank with ID {bank_id} not found.")
        return redirect(url_for('Adminindex'))

# Route to handle the form submission for updating bank details
@app.route('/update_bank/<bank_id>', methods=['POST'])
@login_required
@admin_required
def update_bank(bank_id):
    bank = Bank.query.filter_by(bankID=bank_id).first()
    form = BankCreateForm(request.form, obj=bank)
    if form.validate_on_submit():
        form.populate_obj(bank)  # Update the bank object with the form data
        db.session.commit()
        flash(f"Bank with ID {bank_id} has been updated successfully.")
        return redirect(url_for('Adminindex'))
    else:
        flash("Failed to update bank. Please check your inputs.")
        return render_template('update_bank.html', bankCreateform=form, bank=bank)



from flask import render_template, redirect, url_for

# Route to render the update employee details form
@app.route('/update_employee/<emp_id>', methods=['GET'])
@login_required
@admin_required
def render_update_employee_form(emp_id):
    employee = Employee.query.filter_by(empID=emp_id).first()
    if employee:
        return render_template('update_employee.html', employee_form=EmployeeForm(obj=employee), employee=employee)
    else:
        flash(f"Employee with ID {emp_id} not found.")
        return redirect(url_for('Adminindex'))

# Route to handle the form submission for updating employee details
@app.route('/update_employee/<emp_id>', methods=['POST'])
@login_required
@admin_required
def update_employee(emp_id):
    employee = Employee.query.filter_by(empID=emp_id).first()
    form = EmployeeForm(request.form, obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)  # Update the employee object with the form data
        db.session.commit()
        flash(f"Employee with ID {emp_id} has been updated successfully.")
        return redirect(url_for('Adminindex'))
    else:
        flash("Failed to update employee. Please check your inputs.")
        return render_template('update_employee.html', employee_form=form, employee=employee)

# Route to delete an employee
@app.route('/delete_employee/<emp_id>', methods=['GET'])
@login_required
@admin_required
def delete_employee(emp_id):
    employee_to_delete = Employee.query.filter_by(empID=emp_id).first()
    if employee_to_delete:
        db.session.delete(employee_to_delete)
        db.session.commit()
        flash(f"Employee with ID {emp_id} has been deleted successfully.")
    else:
        flash(f"Employee with ID {emp_id} not found.")
    return redirect(url_for('Adminindex'))


from flask_admin import Admin as admn
from flask_admin.contrib.sqla import ModelView

# Assuming you have the following models: Bank, Employee, Customer, LoanDetails, LoanType, and AdminTable

# Create the Flask-admin instance
admin1 = admn(app, name='AdminTable Panel', template_mode='bootstrap3')

class MyModelView(ModelView):
    def is_accessible(self):
        # Check if the current user is logged in and is an admin
        return current_user.is_authenticated and current_user.user_type=="admin"

# Add views for each model to the admin interface
admin1.add_view(MyModelView(Bank, db.session,))
admin1.add_view(MyModelView(Employee, db.session))
admin1.add_view(MyModelView(Customer, db.session))
admin1.add_view(MyModelView(LoanDetails, db.session))
admin1.add_view(MyModelView(LoanType, db.session))
admin1.add_view(MyModelView(AdminTable, db.session))
admin1.add_view(MyModelView(AllUserTable, db.session))



# @app.route('/admin')
# @loginequired
# @admin_required
# def admin_panel():
#     return admin1.index()

if __name__ == "__main__":
    app.run(debug=True)