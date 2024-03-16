from dotenv import load_dotenv

from multiprocessing import Process, Queue

import logging
logger = logging.getLogger("nospy")

from nosferatu.logger import setup_logging

from nosferatu.listen.listen import listener
from nosferatu.think.think import processor
from nosferatu.reply.reply import sender


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    logger.debug("Starting Nosferatu...")


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
        logger.warning("Terminating...")
        listener_process.terminate()
        # processor_process.terminate()
        # sender_process.terminate()
        listener_process.join()
        # processor_process.join()
        # sender_process.join()
