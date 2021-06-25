import logging
from flask import Flask, url_for, render_template, request
from flask_socketio import SocketIO
import socket
import json

app = Flask(__name__)
socketio = SocketIO(app)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


"""
Basic server implementation, nothing to do here but you can make it better
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path>')
def static_files(path):
    return url_for('static', filename=path)

"""
TODO: Update to retrieve logs from the remote game
"""
@app.route('/info', methods=['GET'])
def display_info():

    return ""

"""
TODO: Update to send commands to the remote game
"""
@socketio.on('command')
def send_commands(json_data):
    # See the log file
    #app.logger.info("Incoming command %s", json)
    localIP     = "localhost"

    localPort   = 20001

    bufferSize  = 1024

    msgFromServer       = "Hello UDP Client"

    #print(json_data)

    # data_str = json.dumps(json_data)


    # json_data = list(json_data)
    # print(len(json_data))
    # for i in range(len(json_data)):
    #     print(json_data)
    
    print(json_data)

    json_data = list(json_data.items())

    a = json_data[0]

    b = json_data[1]

    button = a[1]
    player = b[1]


    print(button, player)
    


    # Create a datagram socket

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]
    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))



    bytesToSend = str.encode(button)
    
    #print("UDP server up and listening")
        # Send command to the game
    
    UDPServerSocket.sendto(bytesToSend, (address))
    pass

"""
Starting App
"""
if __name__ == '__main__':
    socketio.run(app)
