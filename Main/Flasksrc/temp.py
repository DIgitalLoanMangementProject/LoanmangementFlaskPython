#Tells flask-sqlalchemy what database to connect to
# Enter a secret key
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# Initialize flask-sqlalchemy extension
 
# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:adminPass@localhost:3306/yourdbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
 
 
# Initialize app with extension
db.init_app(app)
# Create database within app context
 
with app.app_context():
    db.create_all()

#Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)