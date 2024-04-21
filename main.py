import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any

#
dispatcher = Dispatcher()

ip = "192.168.86.32" # set to the IP of the computer running the server and set the multi play ip to physical
port = 8000 # set to the port the server is running on

# Set up server and client for testing
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient(ip, port)

# Send message and receive exactly one message (blocking)
response = client.send_message("cue/1/start", 1)
print(response)