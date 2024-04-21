import pythonosc as osc
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
import asyncio
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


dispatcher = Dispatcher()
ip = "192.168.86.32" # set to the IP of the computer running the server and set the multi play ip to physical
client_port = 8000 # set to the port the server is running on
server_port = 8001 # set to the port the client is running on
# Set up server and client for testing
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
client = SimpleUDPClient(ip, client_port)




# Send message and receive exactly one message (blocking)
client.send_message("status/go", 1)



def filter_handler(address, *args):
    print(f"{address}: {args}")


dispatcher.map("/status/go", filter_handler)



async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    for i in range(10):
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, server_port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())