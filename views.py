from flask import Blueprint, render_template

web = Blueprint(__name__, "views")

# Route to handle REGISTRATION
@web.route("/register")
def register():
    return render_template("reg.html")

@web.route("/login")
def login():
    return render_template("login.html")
