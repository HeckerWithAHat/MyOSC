import time
all_cues = []

show_end = False

def handle_arr(item):
    global show_end
    global all_cues
    if "Show End" in item[0]:
        show_end = True
        return "END"
    else:
        qnum = (item[0].split(" "))[0].strip("[").strip("]").strip(" ")
        qname = " ".join((item[0].split(" "))[1::])
        all_cues.append([qnum, qname])

def get_cues(client):
    global all_cues
    global show_end
    client.send_message("/select/first", 1)
    while not show_end:
        client.send_message("/select/next", 1) 
    time.sleep(0.1)
    client.send_message("/select/first", 1)
    return all_cues