from pymongo import MongoClient


from nosferatu.common import cprint, Colors

        

def create_invoice():
    invoice_dict = {
        "type": "invoice",
        "message": "Your credits are too low to reply. Pay this invoice to add 100 credits and continue the conversation.",
        "link": "<Invoice Link>",
        "credits": 100
    }
    return invoice_dict


def process_reply(dm):
    return dm + " was processed successfully"


def process_new_command():
    return "New command processed successfully"


def process_balance_command():
    return "Balance command processed successfully"


def process_help_command():
    return "Help command processed successfully"


def get_sender():
    return "user_10101"


def check_credits(sender):
    return 100


def decrease_credits(sender):
    pass



def processor(queue, response_queue):
    client = MongoClient('localhost', 27017)
    db = client['mydatabase']
    collection = db['mycollection']

    while True:
        if not queue.empty():
            document_id = queue.get()
            dm = collection.find_one({"_id": document_id})

            sender = get_sender(dm)
            credits = check_credits(sender)

            # Check if first character of DM is '/'
            if dm[0] == '/':
                command = dm.split(' ')[0][1:]
                command = command.upper()

                if command == 'NEW':
                    response_queue.put(process_new_command())
                elif command == 'BALANCE':
                    response_queue.put(process_balance_command())
                elif command == 'HELP':
                    response_queue.put(process_help_command())
            else:
                if credits > 10:
                    # process reply and place in response queue
                    # stream = ""
                    # for chunk in stream_reply(dm):
                    #     # add chunk to stream
                    #     stream += chunk
                    #     # if double newline in stream (end of paragraph), place that paragraph in response queue
                    #     if "\n\n" in stream:
                    #         paragraph = stream.split("\n\n")[0]
                    #         response_queue.put(paragraph)
                    #         # remove paragraph from stream
                    #         stream = stream.replace(paragraph, "")
                    # place remaining stream in response queue
                    # response_queue.put()

                    response_queue.put(process_reply(dm))
                    decrease_credits(sender)
                else:
                    # generate invoice and place in response queue
                    response_queue.put(create_invoice())

