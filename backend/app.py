from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SocketIO with gevent
socketio = SocketIO(app, async_mode='gevent')
db = SQLAlchemy(app)

#model for storing users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

#model for storing messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)


#----------------Routes----------------------------------------------------------
# index file route
@app.route('/')
def index():
    return render_template('index.html')

# static file route
@app.route('/frontend/<path:filename>')  # Changing the route path for clarity
def serve_static_files(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')), filename)  # Correcting the static path

#route to display all users
@app.route('/users')
def display_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

#route to display all messages
@app.route('/messages')
def display_messages():
    message - Message.query.all()
    return jsonify([{'username': message.username, 'content': message.content}for message in message])
#----------------Routes----------------------------------------------------------


#------------------Websocket Events----------------------------------------------
# websocket event for new users
@socketio.on('new_connection')
def handle_new_connection(data):
    username = data.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
    
    emit('user_connected', {'username':username}, broadcast=True)

# WebSocket event for message broadcasting
@socketio.on('send_message')
def handle_send_message(data):
    message_content = data.get('message')
    username = data.get('username')
    
    #save messages in database
    new_message = Message(content=message_content, username=username)
    db.session.add(new_message)
    db.session.commit()
    emit('recieve_message', {'message':message_content, 'username':username}, broadcast=True)

#------------------Websocket Events----------------------------------------------

# Run the Flask-SocketIO server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
