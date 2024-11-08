from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialisation de la base de données
def init_db():
    with sqlite3.connect("cards.db") as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT NOT NULL UNIQUE,
                card_type TEXT NOT NULL
            )"""
        )

# Route pour ajouter une carte
@app.route("/add_card", methods=["POST"])
def add_card():
    data = request.get_json()
    name = data.get("name")
    serial_number = data.get("serial_number")
    card_type = data.get("card_type")
    try:
        with sqlite3.connect("cards.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cards (name, serial_number, card_type) VALUES (?, ?, ?)",
                (name, serial_number, card_type),
            )
            conn.commit()
        return jsonify({"message": "Carte ajoutée avec succès"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Le numéro de série existe déjà"}), 400

# Route pour rechercher une carte par nom ou numéro de série
@app.route("/search_card", methods=["GET"])
def search_card():
    search_term = request.args.get("search_term")
    with sqlite3.connect("cards.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM cards WHERE name = ? OR serial_number = ?",
            (search_term, search_term),
        )
        card = cursor.fetchone()
    if card:
        return jsonify({"card": {"name": card[1], "serial_number": card[2], "card_type": card[3]}})
    else:
        return jsonify({"message": "Carte non trouvée"}), 404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
