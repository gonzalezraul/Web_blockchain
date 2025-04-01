from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'  # Necesario para manejar sesiones

db = SQLAlchemy(app)

class Criptomoneda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    change_percentage = db.Column(db.Float, default=0.0)  # Nuevo campo para % de cambio

# Clase de usuario para login/registro
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # Nota: para producción, utiliza hashing

with app.app_context():
    db.create_all()
    if Criptomoneda.query.count() == 0:
        criptomonedas = [
            "Bitcoin", "Ethereum", "Cardano", "Solana", "Dogecoin",
            "Polkadot", "Litecoin", "Tether", "Xrp", "Bnb"
        ]
        for nombre in criptomonedas:
            porcentaje = round(random.uniform(-10, 10), 2)  # Genera valores aleatorios entre -10% y 10%
            db.session.add(Criptomoneda(name=nombre, change_percentage=porcentaje))
        db.session.commit()

@app.route('/', methods=['GET'])
def index():
    criptomonedas = Criptomoneda.query.all()
    return render_template('index.html', criptomonedas=criptomonedas)

@app.route('/favorito/<int:id>', methods=['GET','POST'])
def favorito(id):
    criptomoneda = Criptomoneda.query.get(id)
    if criptomoneda:
        criptomoneda.favorite = not criptomoneda.favorite
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/imagen/<int:id>')
def imagen(id):
    imagenes = {
        1: "https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg",
        2: "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg",
        3: "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cardano_Logo.svg",
        4: "https://upload.wikimedia.org/wikipedia/en/b/b9/Solana_logo.png",
        5: "https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png",
        6: "https://upload.wikimedia.org/wikipedia/en/7/7d/Polkadot_cryptocurrency_logo.svg",
        7: "https://upload.wikimedia.org/wikipedia/commons/4/42/Litecoin.svg",
        8: "https://upload.wikimedia.org/wikipedia/en/8/88/Chainlink_Logo.png",
        9: "https://upload.wikimedia.org/wikipedia/en/6/6f/Ripple_logo.png",
        10: "https://upload.wikimedia.org/wikipedia/en/2/25/Stellar_logo.png"
    }
    return redirect(imagenes.get(id, "https://via.placeholder.com/150"))

# Rutas para registro, login y logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         # Verifica si el usuario ya existe
         if User.query.filter_by(username=username).first():
              flash('El usuario ya existe, elige otro.')
              return redirect(url_for('register'))
         new_user = User(username=username, password=password)
         db.session.add(new_user)
         db.session.commit()
         session['username'] = username  # Guarda el nombre en la sesión
         return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         user = User.query.filter_by(username=username, password=password).first()
         if user:
              session['username'] = username
              return redirect(url_for('index'))
         else:
              flash('Credenciales incorrectas')
              return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
