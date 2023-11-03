#from datetime import datetime
from flask import (Flask, render_template, abort, request, redirect, url_for)
from model import db, save_db

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html",
                           message="Here is a message from the view.")

#Please add a page that shows how many times has been viewed.
"""view = 0
@app.route("/views")
def views():
    global view
    view +=1
    return "This page has been viewed " + str(view) + " times."

@app.route("/date")
def date():
    return "This page was served at " + str(datetime.now())"""


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        max_index = len(db)-1
        return render_template("cards.html",
                                card=card,
                                index=index,
                                max_index=max_index)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method=="POST":
        #form has been submitted, process data
        card = {"question" : request.form['question'],
                "answer" : request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template("add_card.html")
    
@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method=="POST":
                #form has been submitted, process data
                del db[index]
                save_db()
                return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html",
                                   card=db[index])
    except IndexError:
        abort(404)