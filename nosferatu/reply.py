from pymongo import MongoClient

from nosferatu.common import cprint, Colors

##################################

def send_response(response, sender):
    cprint(f"Sending response to {sender}: {response}", Colors.ORANGE)

# Sender process
def sender(response_queue):
    while True:
        if not response_queue.empty():
            response = response_queue.get()
            sender = get_sender()
            send_response(response, sender)
