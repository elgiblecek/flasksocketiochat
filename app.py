from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/chat')
def chat():
    return render_template('chat.html')



@app.route('/room')
def room():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('room.html', username=username, room=room)
    

@app.route('/')
def sessions():
    return render_template('home.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('join_room')
def handle_room_join(data):
    app.logger.info(data)
    join_room(data['room'])
    socketio.emit('message_for_joined', data)

@socketio.on('send_msg_toroom')
def handlemsg(data):
    socketio.emit('recivemsg', data)





if __name__ == '__main__':
    socketio.run(app, debug=True)