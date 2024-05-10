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
import json
from utils import get_cues, handle_arr
from flask import Flask, render_template, request, send_from_directory, jsonify, redirect
#
load_dotenv()
app = Flask(__name__)
ip = os.getenv("ip")
server_ip = os.getenv("server_ip")
client_port = (int)(os.getenv("client_port"))
server_port = (int)(os.getenv("server_port"))
cached_time = ""

CURRENT_HANDLER = None

settings = json.load(open('settings/multiplay.json'))

CUE_DESCRIPTION_COMMAND = settings["cue.current.description"]
CUE_GO_COMMAND = settings["cue.go"]
CUE_STOP_COMMAND = settings["cue.stop"]
CUE_JUMP_FWD_COMMAND = settings["cue.jumpfwd"]
CUE_JUMP_BACK_COMMAND = settings["cue.jumpback"]
CUE_TIME_REMAINING_COMMAND = settings["cue.current.time_remaining"]


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
def handle_elapsed(unused_addr, *args):
    global CURRENT_HANDLER
    if CURRENT_HANDLER == "GET_ELAPSED":
        print("\n[SERVER] Received Elapsed Time:", args)
        global cached_time
        cached_time = args[0]
        reset_handler()


local_dispatcher = Dispatcher()
local_dispatcher.map(CUE_DESCRIPTION_COMMAND, handle_response)
local_server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), local_dispatcher)
local_dispatcher.map(CUE_TIME_REMAINING_COMMAND, handle_elapsed)

local_server_thread = threading.Thread(target=local_server.serve_forever)
local_server_thread.start()
client = SimpleUDPClient(ip, client_port)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_all_qs')
def get_all_qs():
    set_handler("GET_CUES")
    all_av_cues = get_cues(client)
    return {"data": all_av_cues}

@app.route('/console')
def console():
    return render_template('console.html')



@app.route('/api/GO')
def api_go():
    cue = request.args.get("cue")
    print("Starting cue " + cue)
    client.send_message(CUE_GO_COMMAND.replace("$cue", cue),0)
    set_handler("GET_ELAPSED")
    
    time.sleep(0.3)
    global cached_time
    temp = cached_time
    cached_time = ""
    timeinsecs = (str)((float)(temp.split(":")[0])*60 + (float)(temp.split(":")[1]))
    return timeinsecs

@app.route('/api/STOP')
def api_stop():
    cue = request.args.get("cue")
    print("Stopping cue " + cue)
    client.send_message(CUE_STOP_COMMAND.replace("$cue", cue),0)

    return cue

@app.route('/api/PANIC')
def api_panic():
    client.send_message(CUE_STOP_COMMAND.replace("$cue", "active"), 1)
    return "It worked, but Relax"


@app.route('/api/FORWARD')
def api_forward():
    cue = request.args.get("cue")
    time = request.args.get("time")
    if (time!=None):
        print("Forwarding cue " + cue + " by " + time)
        client.send_message(CUE_JUMP_FWD_COMMAND.replace("$cue", cue),time)
    else:
        print("Forwarding cue " + cue)
        client.send_message(CUE_JUMP_FWD_COMMAND.replace("$cue", cue),[])
        

    return cue
    


@app.route('/api/REWIND')
def api_rewind():
    cue = request.args.get("cue")
    time = request.args.get("time")
    if (time!=None):
        print("Rewinding cue " + cue + " by " + time)
        client.send_message(CUE_JUMP_BACK_COMMAND.replace("$cue", cue),time)
    else:
        print("Rewinding cue " + cue)
        client.send_message(CUE_JUMP_BACK_COMMAND.replace("$cue", cue),[])
        
   
    return cue


if __name__ == "__main__":
    app.run()


# command =""
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
            # if (len(msg_parts) == 2): 
            #     print("Starting cue " + msg_parts[1])
            #     command = "/cue/" + msg_parts[1] + "/start"
            # else:
            #     print("Starting current cue")
            #     command = "/cue/current/start"
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

