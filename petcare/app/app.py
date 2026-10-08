from flask import Flask, render_template, request, redirect, url_for, flash
import os
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)

app.secret_key = "petcare-flask-mysql"


def conectar_banco():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "cadastro_db"),
        user=os.getenv("DB_USER", "cadastro_user"),
        password=os.getenv("DB_PASSWORD", "cadastro123")
    )


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/cadastro")
def cadastro():

    return render_template("cadastro.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome_responsavel = request.form.get("nome_responsavel", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()

    nome_pet = request.form.get("nome_pet", "").strip()
    tipo = request.form.get("tipo", "").strip()
    raca = request.form.get("raca", "").strip()

    if not nome_responsavel or not telefone or not email:
        flash("Preencha todos os dados do responsável.", "erro")
        return redirect(url_for("cadastro"))

    if not nome_pet or not tipo or not raca:
        flash("Preencha todos os dados do pet.", "erro")
        return redirect(url_for("cadastro"))

    try:

        conexao = conectar_banco()

        cursor = conexao.cursor()

        sql = """
            INSERT INTO cadastros
            (nome_responsavel, telefone, email, nome_pet, tipo, raca)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome_responsavel,
            telefone,
            email,
            nome_pet,
            tipo,
            raca
        )

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()

        conexao.close()

        return redirect(url_for("sucesso"))

    except Error as erro:

        flash(f"Não foi possível realizar o cadastro: {erro}", "erro")

        return redirect(url_for("cadastro"))


@app.route("/sucesso")
def sucesso():

    return render_template("sucesso.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )