from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200))
    job = db.Column(db.String(100))

@app.route("/home", methods=["GET"])
def home():
    form = """
    <h1>Remplissez le formulaire</h1>
    <form action="/submit" method="post">
        <label for="firstname">Prénom:</label><br>
        <input type="text" id="firstname" name="firstname"><br>
        <label for="lastname">Nom:</label><br>
        <input type="text" id="lastname" name="lastname"><br>
        <label for="age">Âge:</label><br>
        <input type="number" id="age" name="age"><br>
        <label for="email">E-mail:</label><br>
        <input type="email" id="email" name="email"><br>
        <label for="job">Emploi:</label><br>
        <input type="text" id="job" name="job"><br><br>
        <input type="submit" value="Soumettre">
    </form>
    """
    return form


@app.route("/users", methods=["POST"])
def create_user():
    data = request.form
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    age = data.get("age")
    email = data.get("email")
    job = data.get("job")

    if not all([firstname, lastname, age, email, job]):
        return "Tous les champs doivent être fournis."

    new_user = User(
        firstname=firstname,
        lastname=lastname,
        age=age,
        email=email,
        job=job
    )
    db.session.add(new_user)
    db.session.commit()

    return "Utilisateur créé avec succès."


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return '{"message": "Utilisateur non trouvé."}'
    
    data = request.json
    user.firstname = data.get("firstname", user.firstname)
    user.lastname = data.get("lastname", user.lastname)
    user.age = data.get("age", user.age)
    user.email = data.get("email", user.email)
    user.job = data.get("job", user.job)
    
    db.session.commit()
    
    return '{"message": "Utilisateur mis à jour avec succès."}'

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return '{"message": "Utilisateur non trouvé."}'
    
    db.session.delete(user)
    db.session.commit()
    
    return '{"message": "Utilisateur supprimé avec succès."}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
