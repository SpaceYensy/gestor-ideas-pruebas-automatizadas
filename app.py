from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "clave-secreta-123"

DB = os.path.join(os.path.dirname(__file__), "ideas.db")

USUARIO_VALIDO = "admin"
CONTRASENA_VALIDA = "admin123"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        contrasena = request.form.get("contrasena", "")

        if usuario == "" or contrasena == "":
            error = "Debes llenar todos los campos"
        elif usuario == USUARIO_VALIDO and contrasena == CONTRASENA_VALIDA:
            session["usuario"] = usuario
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    error = None
    conn = get_db()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if titulo == "":
            error = "El titulo es obligatorio"
        elif len(titulo) > 100:
            error = "El titulo no puede tener mas de 100 caracteres"
        else:
            conn.execute(
                "INSERT INTO ideas (titulo, descripcion, categoria) VALUES (?, ?, ?)",
                (titulo, descripcion, categoria)
            )
            conn.commit()

    buscar = request.args.get("buscar", "")
    if buscar:
        ideas = conn.execute(
            "SELECT * FROM ideas WHERE titulo LIKE ?", ('%' + buscar + '%',)
        ).fetchall()
    else:
        ideas = conn.execute("SELECT * FROM ideas").fetchall()

    conn.close()
    return render_template(
        "dashboard.html", ideas=ideas, error=error, usuario=session["usuario"], buscar=buscar
    )


@app.route("/editar/<int:idea_id>", methods=["GET", "POST"])
def editar(idea_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    error = None

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if titulo == "":
            error = "El titulo es obligatorio"
        elif len(titulo) > 100:
            error = "El titulo no puede tener mas de 100 caracteres"
        else:
            conn.execute(
                "UPDATE ideas SET titulo=?, descripcion=?, categoria=? WHERE id=?",
                (titulo, descripcion, categoria, idea_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("dashboard"))

    idea = conn.execute("SELECT * FROM ideas WHERE id=?", (idea_id,)).fetchone()
    conn.close()

    if idea is None:
        return redirect(url_for("dashboard"))

    return render_template("edit.html", idea=idea, error=error)


@app.route("/eliminar/<int:idea_id>")
def eliminar(idea_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM ideas WHERE id=?", (idea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)