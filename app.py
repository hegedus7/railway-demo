import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# A Railway automatikusan beállítja a DATABASE_URL környezeti változót
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')

# A PostgreSQL URL formátum javítása SQLAlchemy-hez (ha 'postgres://'-al kezdődne)
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Adatbázis modell létrehozása (egy 'User' nevű tábla)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

# Táblák létrehozása az adatbázisban az alkalmazás indításakor
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Ha még üres az adatbázis, beszúrunk egy teszt adatot
    if not User.query.first():
        test_user = User(username="Railway_Postgres_User")
        db.session.add(test_user)
        db.session.commit()
    
    # Kiolvassuk a felhasználót a PostgreSQL adatbázisból
    user = User.query.first()
    return f"<h1>Sikeres PostgreSQL kapcsolat! 🎉</h1><p>Adatbázisból kiolvasott elem: <b>{user.username}</b> (ID: {user.id})</p>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
