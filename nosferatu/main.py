import os
import json
import argparse
import logging
from logging.handlers import QueueHandler, QueueListener
logger = None

from multiprocessing import Process, Queue
from contextlib import contextmanager

from nosferatu.listen.listen import init_listener
from nosferatu.think.think import init_processor
from nosferatu.reply.reply import init_sender


from nosferatu.logger import ColoredFormatter, set_color, YELLOW, WHITE


def setup_logging(log_queue):
    debug = os.getenv("DEBUG", False)
    if debug:
        log_format = f"%(levelname)s | ({set_color(YELLOW)}%(filename)s @ %(lineno)d{set_color(WHITE)}) | %(message)s"
    else:
        log_format = "%(levelname)s | %(message)s"


    # log_queue = Queue()
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) # TODO

    # These logs will be shown in the console
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(log_format, datefmt="%Y/%m/%d %H:%M.%S")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Then create a queue listener with a default console handler and start it
    queue_listener = QueueListener(log_queue, console_handler)
    queue_listener.start()





def load_settings(name):
    bot_dir = os.path.join(os.path.expanduser("~"), "bots")

    settings_file = os.path.join(bot_dir, name, "settings.json")
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                logger.debug(f"Loaded settings.json for {name}")
                return settings
        except json.JSONDecodeError:
            logger.error(f"settings.json not valid for {name}")
    else:
        logger.warning(f"settings.json not found for {name}")
        exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="", help="Input your name")
    args = parser.parse_args()

    if args.name == "":
        print("Please provide a name with --name")
        exit(1)

    # log_queue = Queue()
    # global logger
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG) # TODO

    # # These logs will be shown in the console
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(logging.Formatter('[%(levelname)s/%(processName)s] %(message)s'))
    # logger.addHandler(console_handler)

    # # Then create a queue listener with a default console handler and start it
    # queue_listener = QueueListener(log_queue, console_handler)
    # queue_listener.start()

    log_queue = Queue()
    setup_logging(log_queue)

    settings = load_settings(args.name)

    queue = Queue()
    response_queue = Queue()


    listener_process = Process(target=init_listener, args=(settings, queue, log_queue, ))
    processor_process = Process(target=init_processor, args=(settings, queue, response_queue, log_queue, ))
    sender_process = Process(target=init_sender, args=(settings, response_queue, log_queue, ))

    listener_process.start()
    processor_process.start()
    sender_process.start()

    try:
        listener_process.join()
        processor_process.join()
        sender_process.join()

    except KeyboardInterrupt:
        logger.warning("Terminating...")
        listener_process.terminate()
        processor_process.terminate()
        sender_process.terminate()
        listener_process.join()
        processor_process.join()
        sender_process.join()
