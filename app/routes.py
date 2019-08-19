from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Agarwal Ji'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Rishabh', user=user, posts=posts)


# @app.route lines above the function are decorators
# A common pattern with decorators is to use them to register functions as callbacks for certain events
# This means that when a web browser requests either of these two URLs,
# Flask is going to invoke this function and pass the return value of it back to the browser as a response.
