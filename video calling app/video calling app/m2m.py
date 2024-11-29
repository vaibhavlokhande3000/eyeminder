import time
from flask import Flask, redirect, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
import uuid
# new import
import fetch_frame_data as ffd
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app, 
                    cors_allowed_origins="*",
                    #max_http_buffer_size=9999999999
                    )

rooms = {}  # For simplicity, store rooms in-memory

@app.route('/create_room', methods=['POST'])
def create_room():
    room_id = uuid.uuid4().hex[:8] # short unique id for room
    if room_id in rooms:
        return jsonify(success=False, message="Room already exists"), 400
    rooms[room_id] = {"participants": []}
    return jsonify({
        "success": True,
        "room_id": room_id
    })

@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    return jsonify(list(rooms.keys()))

@app.route('/delete_room/<room_id>', methods=['GET'])
def delete_room(room_id):
    del rooms[room_id]
    return jsonify({
        "success": True,
        "message": "Room deleted"
    })



@socketio.on('join')
def on_join(data):
    username = data['username']
    room_id = data['room_id']
    if room_id not in rooms:
        return {"success": False, "message": "Room not found"}
    join_room(room_id)
    rooms[room_id]["participants"].append(username)

    # Notify other users in the room about the new user
    for participant in rooms[room_id]["participants"]:
        if participant != username:
            socketio.emit('user_joined', {"username": username, "userId": request.sid}, room=participant)
            time.sleep(5)

    print(f"User {username} has joined room {room_id}")

    # Notify other users in the room about the new user
    socketio.emit('user_joined', {"username": username, "userId": request.sid}, room=room_id)
    

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room_id = data['room_id']
    if room_id not in rooms:
        return {"success": False, "message": "Room not found"}
    leave_room(room_id)
    rooms[room_id]["participants"].remove(username)

    socketio.emit('user_left', {"username": username, "userId": request.sid}, room=room_id)
    

@socketio.on('remote_data')
def data_transfer(data):
    # New Change
    socketio.emit('render_data', {"data":data},include_self=False)


@socketio.on('signal')
def on_signal(data):
    target_user = data['userId']
    room_id = data['room_id']
    signal = data['signal']

    print(f"Signal from {request.sid} to {target_user}")
    # Send the signal to the specified user in the room
    socketio.emit('signal', {"userId": request.sid, "signal": signal}, room=target_user)

# changed code start

def decode_base64_image(data):
    """Decode a base64-encoded image and return it as a NumPy array."""
    header, encoded = data.split(',', 1)
    decoded = base64.b64decode(encoded)
    image = Image.open(BytesIO(decoded))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# def decode_base64_image(base64_string):
#     """Decodes a base64 encoded image into a NumPy array."""
#     try:
#         img_data = base64.b64decode(base64_string)
#         nparr = np.frombuffer(img_data, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
#         # Check if the image is valid
#         if img is None:
#             print("Failed to decode image.")
#             return None
#         return img
#     except Exception as e:
#         print(f"Error decoding base64 image: {e}")
#         return None

@socketio.on('frame')
def handle_frame(data):
    if 'image' in data and data['image']:
        try:
            # Decode the incoming base64 image data
            frame = decode_base64_image(data['image'])
            # print("frame : ",type(frame))
            # Check if the frame was decoded successfully
            if frame is None or frame.size == 0:
                raise ValueError("Decoded image is empty or invalid.")
            
            # print("\nframe received\n")
            
            processed_frame_data = ffd.process_frame(True, frame)
            # print("frame data : ",type(processed_frame_data))
 
            # Send back the processed frame
            emit('frame_data', processed_frame_data)
        except Exception as e:
            print(f"Error processing the frame: {e}")
            emit('frame_data', {'error': 'Failed to process frame'})
    else:
        print("No image data received.")
        emit('frame_data', {'error': 'No frame data received'})

    # """Process the incoming frame and send back the processed frame."""
    # frame = decode_base64_image(data['image'])

    # print("\nframe received\n")

    # # Example: Apply a grayscale effect
    # # processed_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # processed_frame_data = ffd.process_frame(True,frame)

    # # Send back the processed frame
    # emit('frame_data', processed_frame_data)
# changed code end


@app.route('/room_join/<room_id>')
def room_join(room_id):
    if room_id in rooms.keys():
        return render_template('m2m_2.html', room_id=room_id)
    
    return redirect('/')

@app.route('/')
def index():
    return render_template('m2m_1.html')

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port='5000',debug=True)
