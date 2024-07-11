from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from models import Task, User

app = Flask(__name__)
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        task_name = request.form["task_name"]
        Task.create(name=task_name)
        return redirect(url_for("all_tasks"))
    return render_template("create.jinja2")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["name"]
        try:
            user = User.get(User.name==username)
            if pbkdf2_sha256.verify(request.form["password"], user.password):
                session["username"] = username
                return redirect(url_for("all"))
        except User.DoesNotExist:
            return render_template("login.jinja2", error="User was not found")
    return render_template("login.jinja2")

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        username = session["username"]
        user = User.get(User.name==username)
        task_id = request.form["task_id"]
        task = Task.get(Task.id == task_id)
        task.performed_by = user
        task.performed = datetime.now()
        task.save()

    incomplete_tasks = Task.select().where(Task.performed == None)
    return render_template("incomplete.jinja2", tasks=incomplete_tasks)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="localhost", port=port)