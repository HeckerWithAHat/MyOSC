import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
import os
from dotenv import load_dotenv
import threading
import time
import signal
import sys
#
load_dotenv()

ip = os.getenv("ip")
port = 8000

def signal_handler(sig, frame):
    print('\nShutting Down OSC!')
    local_server.shutdown()
    local_server_thread.join()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
def handle_response(unused_addr, *args):
    print("\nReceived response:", args)

local_dispatcher = Dispatcher()
local_dispatcher.map("/status/current/qdesc", handle_response)
local_server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 2000), local_dispatcher)

local_server_thread = threading.Thread(target=local_server.serve_forever)
local_server_thread.start()

client = SimpleUDPClient(ip, port)
command =""
while True:
    message = input("Enter command: ")
    args = input("Enter args: ").split(" ")
    msg_parts = message.split(" ")
    match msg_parts[0]:
        case "ADVANCE":
            print("Advancing cue")
            command = "/select/next"
        case "BACK":
                print("Going back cue")
                command = "/select/prev"
        case "GO":
            if (len(msg_parts) == 2): 
                print("Starting cue " + msg_parts[1])
                command = "/cue/" + msg_parts[1] + "/start"
            else:
                print("Starting current cue")
                command = "/cue/current/start"
        case "STOP":
            if (len(msg_parts) == 2): 
                print("Stopping cue " + msg_parts[1])
                command = "/cue/" + msg_parts[1] + "/stop"
            else:
                print("Stopping current cue")
                command = "/cue/current/stop"
        case "SELECT":
            if (len(msg_parts) == 2): 
                print("Selecting cue " + msg_parts[1])
                command = "/select/" + msg_parts[1]
            else:
                print("Invalid command. Please provide a cue number")
                continue
        case "PANIC":
            print("Stopping all cues")
            command = "/cue/active/stop"
        case "REWIND":
            if (len(msg_parts) == 2): 
                print("Rewinding cue " + msg_parts[1])
                command = "/cue/" + msg_parts[1] + "/jumpback"
            else:
                print("Rewinding current cue")
                command = "/cue/current/jumpback"
        case _  :
            print("Invalid command")
            continue
    client.send_message(command, args)