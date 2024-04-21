import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.udp_client import SimpleUDPClient
import os
from dotenv import load_dotenv 
#
dispatcher = Dispatcher()
load_dotenv()

ip = os.getenv("ip") # set to the IP of the computer running the server and set the multi play ip to physical
port = 8000 # set to the port the server is running on

# Set up server and client for testing

client = SimpleUDPClient(ip, port)

response = client.send_message("cue/current/start", 1)
print(response)