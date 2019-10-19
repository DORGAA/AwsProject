from flask import Flask, render_template, request, session, g, redirect, url_for, jsonify
import flask_socketio
import flask_login
import sqlite3
from models.colonne import Colonne,ColonneForDisplay
from models.tableaux import Tableau,TableauForDisplay
from models.user import User, UserForLogin, ConnectedUser
from models.post import Post, PostForDisplay
import uuid

DATABASE = '.data/db.sqlite'
app = Flask(__name__)
app.secret_key = 'mysecret!'
io = flask_socketio.SocketIO(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_get'

@login_manager.user_loader
def load_user(email):
    db = get_db()
    cur = db.cursor()
    return UserForLogin.getByEmail(cur, email)

##############################################################################
#                BOILERPLATE CODE (you can essentially ignore this)          #
##############################################################################

def get_db():
    """Boilerplate code to open a database
    connection with SQLite3 and Flask.
    Note that `g` is imported from the
    `flask` module."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.teardown_appcontext
def close_connection(exception):
    """Boilerplate code: function called each time 
    the request is over."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
##############################################################################
#                APPLICATION CODE (read from this point!)                    #
##############################################################################

@app.route("/")
@flask_login.login_required
def home():
   db = get_db()
   cur = db.cursor()
   tableau_list=TableauForDisplay.getAll(cur)
   return render_template('index.html',tableau = tableau_list )
  

@app.route("/login", methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember_me')
    if not email or not password:
        return render_template(
          'login.html',
          error_msg="Please provide your email and your password.",
        )

    db = get_db()
    cur = db.cursor()
    
    user = UserForLogin.getByEmail(cur, email)
    if user is None or not user.check_password(password):
        return render_template(
          'login.html',
          error_msg="Authentication failed",
        )

    flask_login.login_user(user, remember=remember)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

  
@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if not email or not name or not password1 or not password2:
        return render_template(
          'register.html',
          error_msg="Please provide your email, name and password.",
        )


    if password1 != password2:
        return render_template(
          'register.html',
          error_msg="The passwords do not match!",
        )
      
    user = User(name=name, email=email, password=password1)
    db = get_db()
    cur = db.cursor()
    try:
        user.insert(cur)
    except sqlite3.IntegrityError:
        return render_template(
          'register.html',
          error_msg="This email is already registered.",
        )
    
    db.commit()
    
    return redirect(url_for('login_get'))

@app.route('/is-email-used/<email>')
def is_email_used(email):
    db = get_db()
    cur = db.cursor()
    
    user = UserForLogin.getByEmail(cur, email)
    free = user is None
        
    return jsonify({"email": email, "free": free})
    
@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login_get'))
  
@app.route('/loged', methods=['GET'])
def loged_get():
    db = get_db()
    cur = db.cursor()
    tableau_list=TableauForDisplay.getAll(cur)
    
    return render_template('index.html',tableau = tableau_list )
  
@app.route('/loged', methods=['POST'])
def loged_post():
  task = request.form.get('task')
 

  tableau = Tableau(str(uuid.uuid4()),task)
  db = get_db()
  cur = db.cursor()
  try:
      tableau.insert(cur)
  except sqlite3.IntegrityError:
    print("error")
  
  db.commit()
  
  tableau_list=TableauForDisplay.getAll(cur)
  #print(tableau_list)
  
  #tableau_list=["123","123"]
  #x=len(tableau_list)
  return render_template('index.html' ,  tableau = tableau_list )


@app.route('/tableau', methods=['GET'])
def tab_get():
    db = get_db()
    cur = db.cursor()
    colonnes_list=ColonneForDisplay.getAllForTab(cur,request.args.get('tab'))
    print(colonnes_list)
    return render_template('tableau.html',tab_id=request.args.get('tab'),colonnes_list=colonnes_list)
  
@app.route('/ajout_colonne', methods=['POST'])
def ajouter_colonne():
    tab_id=request.form.get('tableau')
    colonne_nom=request.form.get('colonne')
    
    
    colonne=Colonne(str(uuid.uuid4()),colonne_nom,tab_id)
    db = get_db()
    cur = db.cursor()
    try:
        colonne.insert(cur)
    except sqlite3.IntegrityError:
      print("error")
    
    db.commit()
        
    
    return redirect("tableau?tab="+tab_id, code=302)
  
    
if __name__ == '__main__':
    io.run(app, debug=True)
