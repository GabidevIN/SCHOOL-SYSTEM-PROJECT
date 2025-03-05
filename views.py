from flask import Blueprint, render_template

web = Blueprint(__name__, "views")

# LOGIN / REGISTER 
@web.route("/login")
def login():
    return render_template("login.html")

@web.route("/home")
def login():
    return render_template("home.html")
