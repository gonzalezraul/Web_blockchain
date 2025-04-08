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
    price = db.Column(db.Float, default=0.0)
    info = db.Column(db.Text, default="")     # Aquí se guarda la información adicional propia de cada criptomoneda.
    acerca = db.Column(db.Text, default="")   # Aquí se guarda la sección 'Acerca de' propia de cada criptomoneda.

# Define el modelo de usuario para evitar errores al referenciar a "User"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.drop_all()
    db.create_all()
    if Criptomoneda.query.count() == 0:
        criptomonedas = [
            {
                "name": "Bitcoin", 
                "price": 78057.97,
                "info": "Información y análisis de Bitcoin.",
                "acerca": "Bitcoin, la primera criptomoneda del mundo, se almacena e intercambia de forma segura en internet a través de un libro de contabilidad distribuido conocido como una cadena de bloques. Los bitcoins se pueden dividir en unidades más pequeñas llamadas satoshis, cada satoshi tiene el valor de 0,00000001 bitcoins."
            },
            {
                "name": "Ethereum", 
                "price": 3000.0,
                "info": "Información, análisis y tendencias de Ethereum.",
                "acerca": "Ethereum es una plataforma informática descentralizada que utiliza ETH (también denominado Ether) para pagar las comisiones de las transacciones (o «gas»). Los desarrolladores pueden usar Ethereum para ejecutar aplicaciones descentralizadas (dapps) y emitir nuevos criptoactivos, conocidos como tokens de Ethereum."
            },
            {
                "name": "Cardano", 
                "price": 1.2,
                "info": "Análisis y datos sobre Cardano.",
                "acerca": "Cardano (ADA) is a blockchain platform built on a proof-of-stake consensus protocol (called Ouroboros) that validates transactions without high energy costs. Development on Cardano uses the Haskell programming language, which is described as enabling Cardano “to pursue evidence-based development for unparalleled security and stability.” The blockchain’s native token, ADA, is named after the 19th century mathematician, Ada Lovelace."
            },
            {
                "name": "Solana", 
                "price": 150.0,
                "info": "Información y análisis de Solana, la red de alto rendimiento.",
                "acerca": "Solana is a decentralized computing platform that uses SOL to pay for transactions. Solana aims to improve blockchain scalability by using a combination of proof of stake consensus and so-called proof of history. As a result, Solana claims to be able to support 50,000 transactions per second without sacrificing decentralization."
            },
            {
                "name": "Dogecoin", 
                "price": 0.16,
                "info": "Noticias y análisis sobre Dogecoin, la criptomoneda meme.",
                "acerca": "Dogecoin (DOGE) se creó en 2013 para ofrecer una alternativa más desenfadada que las criptomonedas tradicionales, como Bitcoin. El nombre Dogecoin y el logotipo del perro de raza shiba inu están inspirados en un meme. A diferencia de Bitcoin, cuya escasez forma parte de su naturaleza, Dogecoin está pensado para ser un activo abundante. Tanto es así que, además de no disponer de un suministro máximo establecido, cada minuto se minan 10 000 monedas nuevas en todo el mundo."
            },
            {
                "name": "Polkadot", 
                "price": 25.0,
                "info": "Análisis y tendencias de Polkadot en el mercado cripto.",
                "acerca": "Polkadot es un protocolo que permite las transferencias de cualquier tipo de datos o activos entre cadenas de bloques. Al unir varias cadenas de bloques, Polkadot trata de ofrecer un mayor grado de seguridad y escalabilidad. DOT es el token de gobernanza del protocolo y se puede usar en procesos de staking para mejorar la seguridad de la red o para conectar o vincular nuevas cadenas."
            },
            {
                "name": "Litecoin", 
                "price": 180.0,
                "info": "Datos, análisis y noticias sobre Litecoin.",
                "acerca": "Litecoin es una criptomoneda que usa un programa de confirmación de pagos más rápido y un algoritmo criptográfico diferente a bitcoin."
            },
            {
                "name": "Tether", 
                "price": 1.0,
                "info": "Información y análisis de Tether, la stablecoin más popular.",
                "acerca": "Tether (USDT) es un token de Ethereum sujeto al valor de un dólar estadounidense (también se denomina stablecoin). El emisor de Tether afirma que cada USDT en circulación está respaldado por reservas bancarias y préstamos por un valor idéntico o superior. Nota importante: Coinbase únicamente es compatible con USDT que se ejecuta en la cadena de bloques de Ethereum (ERC-20). No envíe USDT a Coinbase en ninguna otra cadena de bloques."
            },
            {
                "name": "Xrp", 
                "price": 0.6,
                "info": "Análisis y noticias sobre XRP, la criptomoneda de Ripple.",
                "acerca": "XRP is the native token of the XRP Ledger, and the cryptocurrency used by the Ripple payment network. Built for enterprise use on a global scale, XRP powers cost-efficient cross-border payments."
            },
            {
                "name": "Bnb", 
                "price": 350.0,
                "info": "Información y análisis sobre BNB, la criptomoneda de Binance.",
                "acerca": "Binance Coin is a cryptocurrency used to pay fees on the Binance cryptocurrency exchange. Fees paid in Binance Coin on the exchange receive a discount."
            }
        ]
        for moneda in criptomonedas:
            porcentaje = round(random.uniform(-10, 10), 2)  # Generate random change percentage
            db.session.add(Criptomoneda(
                name=moneda["name"], 
                price=moneda["price"], 
                change_percentage=porcentaje,
                info=moneda["info"],       # Aquí se asigna la información adicional de la criptomoneda.
                acerca=moneda["acerca"]    # Aquí se asigna la sección 'Acerca de' de la criptomoneda.
            ))
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
        3: "https://dynamic-assets.coinbase.com/da39dfe3632bf7a9c26b5aff94fe72bc1a70850bc488e0c4d68ab3cf87ddac277cd1561427b94acb4b3e37479a1f73f1c37ed311c11a742d6edf512672aea7bb/asset_icons/a55046bc53c5de686bf82a2d9d280b006bd8d2aa1f3bbb4eba28f0c69c7597da.png",
        4: "https://upload.wikimedia.org/wikipedia/en/b/b9/Solana_logo.png",
        5: "https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png",
        6: "https://dynamic-assets.coinbase.com/9957ebecd9f4d6a2a4cf877577364e8c9bfb937c7f8385e153fc878e9ed3766a563cdd1a80903f465f50b4edfb5089251e045d362a8fbe5b888b9de18bfcc09a/asset_icons/f786d2f3573f77db841b406bf607ac7ddfe70d533acc6d05f2cb3cb3eab11925.png",
        7: "https://dynamic-assets.coinbase.com/f018870b721574ef7f269b9fd91b36042dc05ebed4ae9dcdc340a1bae5b359e8760a8c224bc99466db704d10a3e23cf1f4cd1ff6f647340c4c9c899a9e6595cd/asset_icons/984a4fe2ba5b2c325c06e4c2f3ba3f1c1fef1f157edb3b8ebbfe234340a157a5.png",
        8: "https://dynamic-assets.coinbase.com/41f6a93a3a222078c939115fc304a67c384886b7a9e6c15dcbfa6519dc45f6bb4a586e9c48535d099efa596dbf8a9dd72b05815bcd32ac650c50abb5391a5bd0/asset_icons/1f8489bb280fb0a0fd643c1161312ba49655040e9aaaced5f9ad3eeaf868eadc.png",
        9: "https://dynamic-assets.coinbase.com/e81509d2307f706f3a6f8999968874b50b628634abf5154fc91a7e5f7685d496a33acb4cde02265ed6f54b0a08fa54912208516e956bc5f0ffd1c9c2634099ae/asset_icons/3af4b33bde3012fd29dd1366b0ad737660f24acc91750ee30a034a0679256d0b.png",
        10: "https://dynamic-assets.coinbase.com/36f266bc4826775268588346777c84c1ae035e7de268a6e124bcc22659f0aa2bf4f66dcad89b2ac978cfdb4d51c2d9f63cf7157769efb500b20ca16a6d5719c7/asset_icons/7deb6ff58870072405c0418d85501c4521c3296e33ef58452be98e4ca592ed19.png"
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

@app.route('/cripto/<int:id>')
def cripto(id):
    cripto = Criptomoneda.query.get_or_404(id)
    return render_template('cripto.html', cripto=cripto)


if __name__ == '__main__':
    app.run(debug=True)
