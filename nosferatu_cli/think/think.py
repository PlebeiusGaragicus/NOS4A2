import time
import logging
from logging.handlers import QueueHandler
logger = None

from pymongo import MongoClient

from nosferatu_cli.think.invoice import create_invoice, check_credits, decrease_credits
from nosferatu_cli.think.inference import process_reply
from nosferatu_cli.think.commands import (
    process_new_command,
    process_balance_command,
    process_help_command
)


def setup_logging(log_queue):
    queue_handler = QueueHandler(log_queue)
    global logger
    logger = logging.getLogger("thinker")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)



def init_processor(settings_json, queue, response_queue, log_queue):
    setup_logging(log_queue)
    logger.info("Processor started for %s", settings_json)


    # client = MongoClient('localhost', 27017)
    # db = client['mydatabase']
    # collection = db['mycollection']

    while True:
        if not queue.empty():
            inter_process_message = queue.get()
            # {
                    # "pubkey": from_pub,
                    # "message": clear_text,
                    # "relay": event_msg.url,
            # }

            # TODO: check if user is on block list

            event_to_process = str(inter_process_message['message'])
            logger.info(f"New msg in queue: `{event_to_process}`")

            reply = {
                "pubkey": inter_process_message['pubkey'],
                "content": None,
                "relay": inter_process_message['relay'],
                "event_id": inter_process_message['event_id'],
            }

            if event_to_process[0] == '/': # commands
                command = event_to_process.split(' ')[0][1:]
                command = command.upper()
                logger.debug("COMMAND: %s", command)

                if command == 'NEW':
                    reply.content = process_new_command()
                elif command == 'BALANCE':
                    reply.content = process_balance_command()

                # elif command == 'HELP':
                    # reply = process_help_command()
                    # response_queue.put( reply )
                else:
                    # reply.content = f"Unknown command: {command}"
                    reply.content = process_help_command()

            else:
                reply['content'] = process_reply(event_to_process)

            response_queue.put( reply )







    # while True:
    #     if not queue.empty():
    #         document_id = queue.get()
    #         dm = collection.find_one({"_id": document_id})

    #         sender = get_sender(dm)
    #         credits = check_credits(sender)

    #         # Check if first character of DM is '/'
    #         if dm[0] == '/':
    #             command = dm.split(' ')[0][1:]
    #             command = command.upper()

    #             if command == 'NEW':
    #                 response_queue.put(process_new_command())
    #             elif command == 'BALANCE':
    #                 response_queue.put(process_balance_command())
    #             elif command == 'HELP':
    #                 response_queue.put(process_help_command())
    #         else:
    #             if credits > 10:
    #                 # process reply and place in response queue
    #                 # stream = ""
    #                 # for chunk in stream_reply(dm):
    #                 #     # add chunk to stream
    #                 #     stream += chunk
    #                 #     # if double newline in stream (end of paragraph), place that paragraph in response queue
    #                 #     if "\n\n" in stream:
    #                 #         paragraph = stream.split("\n\n")[0]
    #                 #         response_queue.put(paragraph)
    #                 #         # remove paragraph from stream
    #                 #         stream = stream.replace(paragraph, "")
    #                 # place remaining stream in response queue
    #                 # response_queue.put()

    #                 response_queue.put(process_reply(dm))
    #                 decrease_credits(sender)
    #             else:
    #                 # generate invoice and place in response queue
    #                 response_queue.put(create_invoice())
