from flask import Flask, render_template, request, redirect
from werkzeug.utils import redirect
from mysqlconnection import connectToMySQL # import the function that will return an instance of a connection

app = Flask(__name__)

@app.route("/users")
def users():
    mysql = connectToMySQL("users_with_flask")
    users = mysql.query_db('SELECT * FROM users;')
    return render_template("users.html", all_users=users)

@app.route("/users/new")
def new_users_route():
    return render_template("add_a_new_user.html")

@app.route("/users/create", methods=["POST"])
def new_user():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        'fn': request.form["fname"],
        'ln': request.form["lname"],
        'em': request.form["email"]
    }
    db = connectToMySQL("users_with_flask")
    db.query_db(query,data)
    return redirect("/users")

@app.route("/users/<id>")
def show_user(id):
    query = "SELECT * FROM users WHERE id = %(identification)s"
    data = {
        'identification': id
    }
    db = connectToMySQL("users_with_flask")
    user = db.query_db(query,data)
    return render_template("show_user.html", user_data = user)

@app.route("/users/<id>/edit")
def edit_user(id):
    query = "SELECT * FROM users WHERE id = %(identification)s"
    data = {
        'identification': id
    }
    db = connectToMySQL("users_with_flask")
    user = db.query_db(query,data)
    return render_template("edit_user.html", user_data = user)
    
@app.route("/users/<id>/update", methods=["POST"])
def user_update(id):
    query = "UPDATE `users_with_flask`.`users` SET `first_name` = %(fname)s, `last_name` = %(lname)s, `email` = %(email)s, `updated_at` = NOW() WHERE (`id` = %(id)s);"
    data = {
        'id': id,
        'fname': request.form["fname"],
        'lname': request.form["lname"],
        'email': request.form["email"]
    }
    db = connectToMySQL("users_with_flask")
    db.query_db(query,data)
    return redirect("/users")

@app.route("/users/<id>/delete")
def delete_user(id):
    query = "DELETE FROM `users_with_flask`.`users` WHERE (`id` = %(id)s);"
    data = {
        'id': id
    }
    db = connectToMySQL("users_with_flask")
    db.query_db(query, data)
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)
