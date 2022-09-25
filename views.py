"""from flask import Blueprint, render_template

#name of file = Blueprint(__name__, name of blueprint)
views = Blueprint(__name__, "views")

#creating a route /hello
#adding 2 methods this route can accept
    #instead of only 'GET' by DEFAULT now we can 'POST' TOO
        #'POST' = SEND DATA TO DATABASE
@views.route("/", method = ['POST', 'GET'])
def home():
    #rendering html template and giving it variable name = "javi"
    return render_template("index.html")"""