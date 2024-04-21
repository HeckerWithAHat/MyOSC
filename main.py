import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any

#
dispatcher = Dispatcher()



# Set up server and client for testing
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("127.0.0.1", 8000)

# Send message and receive exactly one message (blocking)
response = client.send_message("cue/go", 1)
print(response)