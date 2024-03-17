from multiprocessing import Process, Queue
from pymongo import MongoClient


def listener(queue):
    while True:
        dm = get_dm()
        client = MongoClient('localhost', 27017)
        db = client['mydatabase']
        collection = db['mycollection']
        inserted_document = collection.insert_one(dm)
        queue.put(inserted_document.inserted_id)


def processor(queue, response_queue):
    while True:
        if not queue.empty():
            document_id = queue.get()
            client = MongoClient('localhost', 27017)
            db = client['mydatabase']
            collection = db['mycollection']
            dm = collection.find_one({"_id": document_id})

            sender = get_sender()
            credits = check_credits(sender)

            # Check if first character of DM is '/'
            if dm[0] == '/':
                command = get_command(dm)
                if command == 'NEW':
                    response_queue.put(process_new_command())
                elif command == 'BALANCE':
                    response_queue.put(process_balance_command())
                elif command == 'HELP':
                    response_queue.put(process_help_command())
            else:
                if credits == 0:
                    # generate invoice and place in response queue
                    response_queue.put(create_invoice())
                else:
                    # process reply and place in response queue
                    response_queue.put(process_reply(dm))
                decrease_credits(sender)


def sender(response_queue):
    while True:
        if not response_queue.empty():
            response = response_queue.get()
            sender = get_sender()
            send_response(response, sender)

if __name__ == "__main__":
    queue = Queue()
    response_queue = Queue()

    # Start the processes
    Process(target=listener, args=(queue,)).start()
    Process(target=processor, args=(queue, response_queue)).start()
    Process(target=sender, args=(response_queue,)).start()
