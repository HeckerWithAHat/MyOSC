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
while True:
    message = input("Enter command: ")
    msg_parts = message.split(" ")
    if msg_parts[0] == "ADVANCE":
        if msg_parts[1] == "cue":
            print("Advancing cue")
            client.send_message("/select/next", 1)
    if msg_parts[0] == "BACK":
        if msg_parts[1] == "cue":
            print("Going back cue")
            client.send_message("/select/prev", 1)
    if msg_parts[0] == "GO":
        print("Starting cue")
        client.send_message("/cue/current/start", 1)
    if msg_parts[0] == "STOP":
        print("Stopping cue")
        client.send_message("/cue/current/stop", 1)

    rsp = client.send_message(message, 1)
