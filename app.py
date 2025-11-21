from flask import Flask, render_template, request, redirect, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = "secreto"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contacts(name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone)
            )
            conn.commit()
    except Exception as e:
        flash(f"Error al guardar: {e}")
    finally:
        conn.close()

    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
            rows = cursor.fetchall()
    except Exception as e:
        rows = []
        flash(f"Error al cargar contactos: {e}")
    finally:
        conn.close()

    return render_template("contacts.html", contacts=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
