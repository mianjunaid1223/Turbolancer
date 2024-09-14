from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
import pymongo
from datetime import datetime
import pytz

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

client = pymongo.MongoClient("mongodb+srv://junaidiqbal:allahsadaro@junaid.lkpmjko.mongodb.net/?retryWrites=true&w=majority")
chat = client["chat"]
messages_collection = chat["messages"]

users = {}

@app.route('/chat')
def index():
    return render_template('playground.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    users[request.sid] = {'username': username, 'room': room}
    emit('status', {'msg': f'{username} has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room.'}, room=room)
    if request.sid in users:
        del users[request.sid]

@socketio.on('disconnect')
def on_disconnect():
    user = users.get(request.sid)
    if user:
        username = user['username']
        room = user['room']
        leave_room(room)
        emit('status', {'msg': f'{username} has disconnected.'}, room=room)
        del users[request.sid]

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    timestamp = datetime.now(pytz.utc)
    print(f'Received message: {message} in room: {room} from {username}')
    message_data = {
        "room": room,
        "message": message,
        "username": username,
        "timestamp": timestamp
    }
    messages_collection.insert_one(message_data)
    emit('response', {'message': message, 'username': username, 'timestamp': timestamp.isoformat()}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
