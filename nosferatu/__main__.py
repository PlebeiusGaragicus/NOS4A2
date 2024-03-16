from dotenv import load_dotenv

from multiprocessing import Process, Queue

import logging
from nosferatu.logger import setup_logging

from nosferatu.common import cprint, Colors
from nosferatu.listen import listener
from nosferatu.process import processor
from nosferatu.reply import sender


if __name__ == "__main__":
    cprint("...the bots are coming...", Colors.GREEN)
    load_dotenv()

    setup_logging()
    logger = logging.getLogger("nospy")

    bots = [
        "NOSFATTY"
    ]

    queue = Queue()
    # response_queue = Queue()

    # Start the processes
    listener_process = Process(target=listener, args=(queue,))
    # processor_process = Process(target=processor, args=(queue, response_queue))
    # sender_process = Process(target=sender, args=(response_queue,))

    listener_process.start()
    # processor_process.start()
    # sender_process.start()

    try:
        listener_process.join()
        # processor_process.join()
        # sender_process.join()

    except KeyboardInterrupt:
        cprint("Terminating...", Colors.RED)
        listener_process.terminate()
        # processor_process.terminate()
        # sender_process.terminate()
        listener_process.join()
        # processor_process.join()
        # sender_process.join()
