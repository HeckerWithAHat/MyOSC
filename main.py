import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
import asyncio
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


dispatcher = Dispatcher()
load_dotenv()

ip = os.getenv("ip") # set to the IP of the computer running the server and set the multi play ip to physical
port = 8000 # set to the port the server is running on

# Set up server and client for testing
from pythonosc.udp_client import SimpleUDPClient


# Send message and receive exactly one message (blocking)
response = client.send_message("cue/1/start", 1)
print(response)