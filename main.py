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
from utils import get_cues, handle_arr
from flask import Flask, render_template, request, send_from_directory, jsonify
#
load_dotenv()
app = Flask(__name__)
ip = os.getenv("ip")
client_port = (int)(os.getenv("client_port"))
server_port = (int)(os.getenv("server_port"))

CURRENT_HANDLER = None

def set_handler(handler):
    global CURRENT_HANDLER
    CURRENT_HANDLER = handler

def reset_handler():
    global CURRENT_HANDLER
    CURRENT_HANDLER = None

def signal_handler(sig, frame):
    print('\nShutting Down OSC!')
    local_server.shutdown()
    local_server_thread.join()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
def handle_response(unused_addr, *args):
    global CURRENT_HANDLER
    if CURRENT_HANDLER == None:
        print("\n[SERVER] Received 'No Handle' Response:", args)
    match CURRENT_HANDLER:
        case "GET_CUES":
            handle_arr(args)


local_dispatcher = Dispatcher()
local_dispatcher.map("/status/current/qdesc", handle_response)
local_server = osc_server.ThreadingOSCUDPServer((ip, server_port), local_dispatcher)

local_server_thread = threading.Thread(target=local_server.serve_forever)
local_server_thread.start()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_all_qs')
def get_all_qs():
    return  get_cues(client)

if __name__ == "__main__":
    app.run()



client = SimpleUDPClient(ip, client_port)


command =""
# while True:
#     message = input("Enter command: ")
#     args = input("Enter args: ").split(" ")
#     msg_parts = message.split(" ")
#     match msg_parts[0]:
#         case "ADVANCE":
#             print("Advancing cue")
#             command = "/select/next"
#         case "BACK":
#                 print("Going back cue")
#                 command = "/select/prev"
#         case "GO":
#             if (len(msg_parts) == 2): 
#                 print("Starting cue " + msg_parts[1])
#                 command = "/cue/" + msg_parts[1] + "/start"
#             else:
#                 print("Starting current cue")
#                 command = "/cue/current/start"
#         case "STOP":
#             if (len(msg_parts) == 2): 
#                 print("Stopping cue " + msg_parts[1])
#                 command = "/cue/" + msg_parts[1] + "/stop"
#             else:
#                 print("Stopping current cue")
#                 command = "/cue/current/stop"
#         case "SELECT":
#             if (len(msg_parts) == 2): 
#                 print("Selecting cue " + msg_parts[1])
#                 command = "/select/" + msg_parts[1]
#             else:
#                 print("Invalid command. Please provide a cue number")
#                 continue
#         case "PANIC":
#             print("Stopping all cues")
#             command = "/cue/active/stop"
#         case "REWIND":
#             if (len(msg_parts) == 2): 
#                 print("Rewinding cue " + msg_parts[1])
#                 command = "/cue/" + msg_parts[1] + "/jumpback"
#             else:
#                 print("Rewinding current cue")
#                 command = "/cue/current/jumpback"
#         case "PCUE":
#             set_handler("GET_CUES")
#             print("Avaliable Cues: ")
#             all_av_cues = get_cues(client)
#             for items in all_av_cues:
#                 print("- [" + items[0] + "] " + items[1])
#             reset_handler()
#             command = "SKIP"
#         case _  :
#             print("Invalid command")
#             continue
#     if command != "SKIP":
#         client.send_message(command, args)
#     command = ""

