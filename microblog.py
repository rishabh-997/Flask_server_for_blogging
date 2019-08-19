from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# The "from app import app" statement imports the app variable that is a member of the app package.
# The app.shell_context_processor decorator registers the function as a shell context function. When the flask shell command runs,
# it will invoke this function and register the items returned by it in the shell session.
