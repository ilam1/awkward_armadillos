'''
awkward_armadillos
P #1: arRESTed development
Kelly Wang, Tiffany Moi, Joyce Wu, Jen Yu
'''
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import nyt_process, omdb_process, auth
import urllib2, json

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def start():
    movie_list = nyt_process.search_results()
    if session.get('username'):
        return render_template('base.html', title = "Home", movies = movie_list, loggedIn=True)
    return render_template('base.html', title = "Home", movies = movie_list, loggedIn=False)

# Login Authentication
@app.route('/login', methods=['GET', 'POST'])
def authentication():
    # if user already logged in, redirect to homepage(base.html)
    if session.get('username'):
        return redirect('profile')
    # user entered login form
    elif request.form.get('login'):
        print "login"
        return auth.login()
    # user didn't enter form
    else:
        return render_template('login.html', title = "Login")


@app.route('/signup', methods=['GET', 'POST'])
def crt_acct():
    if session.get('username'):
        return redirect('base')
    # user entered signup form
    elif request.form.get('signup'):
        return auth.signup()
    else:
        return render_template('signup.html', title = "Signup" )

# Profile page - shows profile stats and (if time, allow them to change password)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('username'):
        flash("Not logged in")
        return redirect(url_for('authentication'))
    else:
        return render_template('profile.html', title = "Profile" , user=session.get('username'), loggedIn=True)

# Logging out
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session.get('username'):
        flash("Not logged in")
    else:
        flash("Logged out")
        session.pop('username')
        return redirect(url_for('authentication'))

@app.route("/search", methods=['POST', 'GET'])
def search():
    movie_list = nyt_process.search_results(request.args["title"])
    if len(movie_list) == 0:
        return render_template("search.html", message = "No Results found.") 
    return render_template("search.html", title = "Search", movies = movie_list)

@app.route("/movie_review", methods=['POST', 'GET'])
def get_movie():
    movie = request.form['title'] #refer back for variable_names
    movie = movie.split("\n")
    url = request.form['url']
    url = url.split("\n")
    review = nyt_process.get_review(url[0])
    try:
        info = omdb_process.get_info(movie[0])
        return render_template("movie_review.html", title=movie[0].replace("_", " "), year=info["Year"], genre=info["Genre"], plot=info["Plot"], pic=info["Poster"], review=review)
    except:
        return render_template("movie_review.html", title=movie[0].replace("_", " "), year="N/A", genre="N/A", plot="N/A", pic="N/A", review=review)

if __name__ == "__main__":
    app.debug = True
    app.run()
